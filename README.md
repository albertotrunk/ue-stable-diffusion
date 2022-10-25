# ue-stable-diffusion
UE5 plugin with stable diffusion integration
Just add your model to

"plugins/Dream/models/model.ckpt"

And all add the modules/dependencies you don't have to the file:
"ue-stable-diffusion\Content\Python\init_unreal.py"

line 35:

required = {'Pillow == 9.2.0','einops == 0.4.1', 'omegaconf == 2.2.3'}



![u5sd copy](https://user-images.githubusercontent.com/8300565/197598541-de332abd-9755-45e3-b5da-2fd4a647144e.jpg)
more info in:
https://github.com/albertotrunk/UE5-Dream

Feel free to colaborate!
