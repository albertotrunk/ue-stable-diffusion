import torch
from torch import Tensor

from .optimizer import Optimizer
from typing import List, Optional


class Adadelta(Optimizer):
    r"""Implements Adadelta algorithm.

    .. math::
       \begin{aligned}
            &\rule{110mm}{0.4pt}                                                                 \\
            &\textbf{input}      : \gamma \text{ (lr)}, \: \theta_0 \text{ (params)},
                \: f(\theta) \text{ (objective)}, \: \rho \text{ (decay)},
                \: \lambda \text{ (weight decay)}                                                \\
            &\textbf{initialize} :  v_0  \leftarrow 0 \: \text{ (square avg)},
                \: u_0 \leftarrow 0 \: \text{ (accumulate variables)}                     \\[-1.ex]
            &\rule{110mm}{0.4pt}                                                                 \\
            &\textbf{for} \: t=1 \: \textbf{to} \: \ldots \: \textbf{do}                         \\
            &\hspace{5mm}g_t           \leftarrow   \nabla_{\theta} f_t (\theta_{t-1})           \\
            &\hspace{5mm}if \: \lambda \neq 0                                                    \\
            &\hspace{10mm} g_t \leftarrow g_t + \lambda  \theta_{t-1}                            \\
            &\hspace{5mm} v_t      \leftarrow v_{t-1} \rho + g^2_t (1 - \rho)                    \\
            &\hspace{5mm}\Delta x_t    \leftarrow   \frac{\sqrt{u_{t-1} +
                \epsilon }}{ \sqrt{v_t + \epsilon}  }g_t \hspace{21mm}                           \\
            &\hspace{5mm} u_t  \leftarrow   u_{t-1}  \rho +
                 \Delta x^2_t  (1 - \rho)                                                        \\
            &\hspace{5mm}\theta_t      \leftarrow   \theta_{t-1} - \gamma  \Delta x_t            \\
            &\rule{110mm}{0.4pt}                                                          \\[-1.ex]
            &\bf{return} \:  \theta_t                                                     \\[-1.ex]
            &\rule{110mm}{0.4pt}                                                          \\[-1.ex]
       \end{aligned}

    For further details regarding the algorithm we refer to `ADADELTA: An Adaptive Learning Rate Method`_.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        rho (float, optional): coefficient used for computing a running average
            of squared gradients (default: 0.9)
        eps (float, optional): term added to the denominator to improve
            numerical stability (default: 1e-6)
        lr (float, optional): coefficient that scale delta before it is applied
            to the parameters (default: 1.0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        foreach (bool, optional): whether foreach implementation of optimizer is used (default: None)
        maximize (bool, optional): maximize the params based on the objective, instead of
            minimizing (default: False)

    .. _ADADELTA\: An Adaptive Learning Rate Method:
        https://arxiv.org/abs/1212.5701
    """

    def __init__(self, params, lr=1.0, rho=0.9, eps=1e-6, weight_decay=0,
                 foreach: Optional[bool] = None, *, maximize: bool = False):
        if not 0.0 <= lr:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if not 0.0 <= rho <= 1.0:
            raise ValueError("Invalid rho value: {}".format(rho))
        if not 0.0 <= eps:
            raise ValueError("Invalid epsilon value: {}".format(eps))
        if not 0.0 <= weight_decay:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))

        defaults = dict(lr=lr, rho=rho, eps=eps, weight_decay=weight_decay,
                        maximize=maximize, foreach=foreach)
        super(Adadelta, self).__init__(params, defaults)

    def __setstate__(self, state):
        super().__setstate__(state)
        for group in self.param_groups:
            group.setdefault('foreach', None)
            group.setdefault('maximize', False)

    @torch.no_grad()
    def step(self, closure=None):
        """Performs a single optimization step.

        Args:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            params_with_grad = []
            grads = []
            square_avgs = []
            acc_deltas = []
            lr, rho, eps, weight_decay, foreach, maximize = (group['lr'],
                                                             group['rho'],
                                                             group['eps'],
                                                             group['weight_decay'],
                                                             group['foreach'],
                                                             group['maximize'])

            for p in group['params']:
                if p.grad is None:
                    continue
                params_with_grad.append(p)
                if p.grad.is_sparse:
                    raise RuntimeError('Adadelta does not support sparse gradients')
                grads.append(p.grad)

                state = self.state[p]

                # Lazy state initialization
                if len(state) == 0:
                    state['step'] = 0
                    state['square_avg'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    state['acc_delta'] = torch.zeros_like(p, memory_format=torch.preserve_format)

                square_avgs.append(state['square_avg'])
                acc_deltas.append(state['acc_delta'])

                state['step'] += 1

            adadelta(params_with_grad,
                     grads,
                     square_avgs,
                     acc_deltas,
                     lr=lr,
                     rho=rho,
                     eps=eps,
                     weight_decay=weight_decay,
                     foreach=foreach,
                     maximize=maximize)

        return loss


def adadelta(params: List[Tensor],
             grads: List[Tensor],
             square_avgs: List[Tensor],
             acc_deltas: List[Tensor],
             # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
             # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
             foreach: bool = None,
             *,
             lr: float,
             rho: float,
             eps: float,
             weight_decay: float,
             maximize: bool):
    r"""Functional API that performs Adadelta algorithm computation.

    See :class:`~torch.optim.Adadelta` for details.
    """

    if foreach is None:
        # Placeholder for more complex foreach logic to be added when value is not set
        foreach = False

    if foreach and torch.jit.is_scripting():
        raise RuntimeError('torch.jit.script not supported with foreach optimizers')

    if foreach and not torch.jit.is_scripting():
        func = _multi_tensor_adadelta
    else:
        func = _single_tensor_adadelta

    func(params,
         grads,
         square_avgs,
         acc_deltas,
         lr=lr,
         rho=rho,
         eps=eps,
         weight_decay=weight_decay,
         maximize=maximize)


def _single_tensor_adadelta(params: List[Tensor],
                            grads: List[Tensor],
                            square_avgs: List[Tensor],
                            acc_deltas: List[Tensor],
                            *,
                            lr: float,
                            rho: float,
                            eps: float,
                            weight_decay: float,
                            maximize: bool):

    for (param, grad, square_avg, acc_delta) in zip(params, grads, square_avgs, acc_deltas):
        grad = grad if not maximize else -grad

        if weight_decay != 0:
            grad = grad.add(param, alpha=weight_decay)

        if torch.is_complex(param):
            square_avg = torch.view_as_real(square_avg)
            acc_delta = torch.view_as_real(acc_delta)
            grad = torch.view_as_real(grad)

        square_avg.mul_(rho).addcmul_(grad, grad, value=1 - rho)
        std = square_avg.add(eps).sqrt_()
        delta = acc_delta.add(eps).sqrt_().div_(std).mul_(grad)
        acc_delta.mul_(rho).addcmul_(delta, delta, value=1 - rho)
        if torch.is_complex(param):
            delta = torch.view_as_complex(delta)
        param.add_(delta, alpha=-lr)


def _multi_tensor_adadelta(params: List[Tensor],
                           grads: List[Tensor],
                           square_avgs: List[Tensor],
                           acc_deltas: List[Tensor],
                           *,
                           lr: float,
                           weight_decay: float,
                           rho: float,
                           eps: float,
                           maximize: bool):

    if len(params) == 0:
        return

    if maximize:
        grads = torch._foreach_neg(grads)

    if weight_decay != 0:
        torch._foreach_add_(grads, params, alpha=weight_decay)

    torch._foreach_mul_(square_avgs, rho)
    torch._foreach_addcmul_(square_avgs, grads, grads, value=1 - rho)

    std = torch._foreach_add(square_avgs, eps)
    torch._foreach_sqrt_(std)

    deltas = torch._foreach_add(acc_deltas, eps)
    torch._foreach_sqrt_(deltas)
    torch._foreach_div_(deltas, std)
    torch._foreach_mul_(deltas, grads)

    torch._foreach_add_(params, deltas, alpha=-lr)

    torch._foreach_mul_(acc_deltas, rho)
    torch._foreach_addcmul_(acc_deltas, deltas, deltas, value=1 - rho)
