#use coding:utf-8
import os
import dlib
from skimage import io
import numpy as np
import cv2
import time as tm
from ai_tools import microsoft_demo as msd
class LDM:
    def __init__(self):
        self.predictor_path="landmarks_68.dat"
        url='http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        self.predictor_path=self.get_model(url,self.predictor_path) 
        self.detector=dlib.get_frontal_face_detector()
        self.predictor=dlib.shape_predictor(self.predictor_path)
        
        self.face_rec_model_path='face_rec.dat'
        url="http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2"
        self.face_rec_model_path=self.get_model(url,self.face_rec_model_path)
        print self.face_rec_model_path 
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        self.CF = msd.init()
    def imread(self,imgpath):
        return io.imread(imgpath)
    def get_part_landmarks(self,shape,start_index,end_index):
        '''
        {   
            dxRange jaw;       // [0 , 16]
            IdxRange rightBrow; // [17, 21]
            IdxRange leftBrow;  // [22, 26]
            IdxRange nose;      // [27, 35]
            IdxRange rightEye;  // [36, 41]
        IdxRange leftEye;   // [42, 47]
        IdxRange mouth;     // [48, 59]
        IdxRange mouth2;    // [60, 67]
        }
        make the shape to be a dict that can easy get  part like jaw,brow,nose,eye,mouth
        '''
        jaw=[]
        for i in range(start_index,end_index):
            #print i+1,shape.part(i)
            jaw.append(np.array((shape.part(i).x,shape.part(i).y)))
        return jaw
  
    def landmark_list(self,img):
        # get all 68 landmarks from the img
        # return the list ldl of the landmark dict ld
        dets = self.detector(img, 1)
        #print("Number of faces detected: {}".format(len(dets)))
        ldl=[]
        facel=[]
        for k,d in enumerate(dets):
            shape=self.predictor(img,d)
            #print k,d
            ld={'help':'jaw,right_brow,left_brow,nose,right_eye,left_eye,mouth,mouth2,all,shape'}
            ld['jaw']=self.get_part_landmarks(shape,0,17)
            ld['right_brow']=self.get_part_landmarks(shape,17,22)
            ld['left_brow']=self.get_part_landmarks(shape,22,27)
            ld['nose']=self.get_part_landmarks(shape,27,36)
            ld['right_eye']=self.get_part_landmarks(shape,36,42)
            ld['left_eye']=self.get_part_landmarks(shape,42,48)
            ld['mouth']=self.get_part_landmarks(shape,48,59)
            ld['mouth2']=self.get_part_landmarks(shape,60,67)
            ld['all']=self.get_part_landmarks(shape,0,67)
            ld['shape']=shape
            ldl.append(ld)
            facel.append(d)
        #for ld in ldl:
        #    print ld['right_eye']
            #print np.array(ld)
        return ldl,facel
    
    def get_model(self,url,predictor_path):
        #predictor_path="landmarks_68.dat"
        #url='http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        if not os.path.exists(predictor_path):
            print os.path.exists("%s.bz2"%(predictor_path))
            if not os.path.exists("%s.bz2"%(predictor_path)):
                os.system('wget -O %s.bz2 %s'%(predictor_path,url))   
            os.system('bunzip2 %s.bz2'%(predictor_path))   
        return predictor_path
    
    def landmarks(self,img):
       
        #predictor_path=get_model() 
        #detector=dlib.get_frontal_face_detector()
        #predictor=dlib.shape_predictor(predictor_path)
        ldl,facel=self.landmark_list(img)
        helptxt='dict[0]_item:jaw,right_brow,left_brow,nose,right_eye,left_eye,mouth,mouth2'
        return ldl,facel,helptxt+',model_paht='+self.predictor_path
    
    def face_area_rate(self,img,facel):
        #the rectangle area of face vs the area of img
        ratel=[]
        for face in facel:
            rate=float(face.width())*float(face.height())
            rate/=float(img.shape(0)) 
            rate/=float(img.shape(1))
            ratel.append(rate) 
        return ratel
    def face_number(self,img,facel):
        face_num=len(facel)
        return face_num
    def draw_rect(self,img,rect):
        x=rect.left()
        y=rect.top()
        w=rect.width()
        h=rect.height()
        #cv2.rectangle(img, (2*w, 2*h), (3*w, 3*h), (255, 0, 0), 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return img
    def face_center_degree(self,img,ldl,facel):
        xdl=[]
        ydl=[]
        mdl=[]
        for face in facel:
            
            xd=float(face.left())+float(face.right())
            xd/=2
            xd=abs(xd-float(img.shape[0])/2)
            xd/=float(img.shape[0])/2
            xd=1-xd

            yd=float(face.top())+float(face.bottom())
            yd/=2
            yd=abs(xd-float(img.shape[1])/2)
            yd/=float(img.shape[1])/2
            yd=1-yd

            md=(xd+yd)*0.5
            xdl.append(xd)
            ydl.append(yd)
            mdl.append(md)
        return xdl,ydl,mdl
    def face_feature(self,img,facel,fc=1):
        #ldl,facel,helptxt=self.landmarks(img)
        ffl=[]
        face_index=0
        for face in facel:
            shape = self.predictor(img, face)
            face_descriptor = self.facerec.compute_face_descriptor(img, shape,fc)
            ffl.append(face_descriptor)
            face_index+=1
        return ffl
    def normalized_sigmoid_fkt(self,a, b, x):
       '''
       Returns array of a horizontal mirrored normalized sigmoid function
       output between 0 and 1
       Function parameters a = center; b = width
       '''
       s= 2/(1+np.exp(b*(x-a)))
       #return 1*(s-min(s))/(max(s)-min(s)) # normalize function to 0-1    
       return s    
    
    def face_compare(self,feature1,feature2,dist_type='cosine'):
        vec1=np.array(feature1)
        #print vec1
        vec2=np.array(feature2)
        if dist_type=='euclidean':
           dist_euclidean=np.linalg.norm(vec1 - vec2)
           dist=dist_euclidean       
        if dist_type=='manhattan':
           dist_manhattan=np.linalg.norm(vec1 - vec2,ord=1)       
           dist=dist_manhattan       
        if dist_type=='chebyshev':
           dist_chebyshev=np.linalg.norm(vec1 - vec2,ord=np.inf)
           dist=dist_chebyshev       
        if dist_type=='cosine':
           dist_cosine=np.dot(vec1,vec2)/(np.linalg.norm(vec1)*(np.linalg.norm(vec2)))
           dist=dist_cosine       
         
        return self.normalized_sigmoid_fkt(0,1.7,dist),dist
    def compare_ffl(self,ff1l,ff2l):
        scorel=[]
        index1l=[]
        index2l=[]
        ic1=0
        ic2=0
        for ff1 in ff1l:
            for ff2 in ff2l:
                #print ic1,ic2
                score,sscore=self.face_compare(ff1,ff2,'euclidean')
                scorel.append(score)
                index1l.append(ic1)
                index2l.append(ic2)
                ic2+=1
            ic1+=1
        return scorel,index1l,index2l
        
    def face_rec(self,img1,img2,threshold=0.8):
        ld1l,face1l,t=self.landmarks(img1)
        ld2l,face2l,t=self.landmarks(img2)
        ff1l=self.face_feature(img1,face1l)
        ff2l=self.face_feature(img2,face2l)
        #print len(ff1l)
        #print len(ff2l)
        scorel,index1l,index2l=self.compare_ffl(ff1l,ff2l)
        #print len(scorel),len(index1l),len(index2l)
        for i in range(0,len(scorel)):
            index=len(scorel)-i-1
            #print index
            if scorel[index]<threshold:
                del scorel[index]
                #del face1l[index]
                #del face2l[index]
                del index1l[index]
                del index2l[index]

        result_dict={'scorel':scorel,
               'face1l':face1l,
               'face2l':face2l,
               'index1l':index1l,
               'incex2l':index2l}
        return result_dict
    def face_rec_ms(self,img1,img2,threshold=0.8):
        cv2.imwrite("tmp1.png",img1)
        cv2.imwrite("tmp2.png",img2)
        scorel=msd.ms_face_verify(self.CF,"tmp1.png","tmp2.png")
        result_dict={'scorel':scorel,
               'face1l':[],
               'face2l':[],
               'index1l':[],
               'incex2l':[]}
        return result_dict
    def has_same_person(self,img1,img2,threshold=0.8,savename='tmp.jpg'):
        ldl1,face1l,t=self.landmarks(img1)
        
        ldl2,face2l,t=self.landmarks(img2)
        ff1l=self.face_feature(img1,face1l);
        ff2l=self.face_feature(img2,face2l);
        scorel,index1l,index2l=self.compare_ffl(ff1l,ff2l)
        sarray=np.array(scorel)
        max_score=0
        if len(sarray)>0:
            max_score=sarray.max()
        sarray=sarray>threshold
        for face in face1l:
            img1=self.draw_rect(img1,face)
        for face in face2l:
            img2=self.draw_rect(img2,face)
        img_a=np.hstack((img1,img2))
        cv2.putText(img_a,'similarity:%.2f'%(max_score),(10,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        print savename

        img_a=cv2.cvtColor(img_a, cv2.COLOR_BGR2RGB)
        cv2.imwrite(savename,img_a)
        return np.sum(sarray),max_score,np.array((len(face1l),len(face2l)))
          


 
    def compare_and_score_ffl(self,ff1l,ff2l,threshold=0.8):
        scorel,index1l,index2l=self.compare_ffl(ff1l,ff2l)
        sarray=np.array(scorel)
        max_score=0
        if len(sarray)>0:
            max_score=sarray.max()
        sarray_t=sarray>threshold
        return np.sum(sarray_t),max_score,sarray
    '''
    def compare2dir(self,imagedir1,imagedir2,max_compare_num=30,score_threshold=0.8):
        timecost=0
        cc1=0
        cc2=0
        compare_num=0
        sameper_num=0
        score_ave=0
        #print imagedir1
        #print os.listdir('/') 
        t1=tm.time() 
        for imf1 in os.listdir(str(imagedir1)):
            #print imf1
            img1=cv2.imread(os.path.join(imagedir1,imf1))
            cc1+=1
            if compare_num>max_compare_num:
                break
            for imf2 in os.listdir(imagedir2):
                #print cc1,cc2,imf2
                img2=cv2.imread(os.path.join(imagedir2,imf2))
                rd=self.face_rec(img1,img2,0.0)
                if len(rd['face1l'])<1 or cc1>3 or cc2>3:
                    cc1=0
                    cc2=0
                    break
                if len(rd['face2l'])<1:
                    cc2=0
                    continue
                #检测到有两次比对，放弃此次比对结果
                #if len(rd['scorel'])>1:
                #    break
                #cc2+=1
                #compare_num+=1
                for score in rd['scorel']:
                #       print score
                       score_ave+=score
                       compare_num+=1
                       cc2+=1
                       if score>score_threshold:
                           sameper_num+=1
                           break
                #print "%d/%d"%(sameper_num,compare_num)
                if compare_num>max_compare_num:
                    break
                    #print ldmer.has_same_person(img1,img2) 
                    #print rd 
                cc2+=1
        score_ave=score_ave/(float(compare_num)+0.0000001)
        t2=tm.time() 
        return float(sameper_num)/(float(compare_num)+0.0000001),score_ave,compare_num,imagedir1.split('/')[-1],imagedir2.split('/')[-1],t2-t1,"http://clt.management.vipkid.com.cn/operation/classroom/classroom/" 
    '''
    def compare2imglist(self,imglist1,imglist2,max_compare_num=30,score_threshold=0.8):
        score_list=np.zeros((100))
        score_list-=2
        t1=tm.time()
        for img1 in imglist1:
            for img2 in imglist2:
               rd=self.face_rec(img1,img2,0.0) 
               score=0
               if len(rd['scorel'])>0:
                   score=rd['scorel'][0]       
               else:
                   score=-1
               score_list.append(score)
        t2=tm.time()
        return score_list,t2-t1
        
    def compare2dir(self,imagedir1,imagedir2,max_compare_num=30,score_threshold=0.8):
        timecost=0
        cc1=0
        cc2=0
        compare_num=0.0
        sameper_num=0.0
        score_ave=0.0
        max_see_images=50
        see_images1=0
        see_images2=0
        #print imagedir1
        #print os.listdir('/') 
        t1=tm.time()
        for imf1 in os.listdir(str(imagedir1)):
            #print imf1
            img1=cv2.imread(os.path.join(imagedir1,imf1))
            cc1+=1
            if compare_num>max_compare_num or see_images1>max_see_images or see_images2>max_see_images:
                break
            for imf2 in os.listdir(imagedir2):
                print cc1,cc2,compare_num,see_images1,see_images2,imf1,imf2
                img2=cv2.imread(os.path.join(imagedir2,imf2))
                rd=self.face_rec(img1,img2,0.0)
                print rd
                if compare_num>max_compare_num or see_images1>max_see_images or see_images2>max_see_images:
                    break
                if len(rd['face1l'])<1 or cc1>3 or cc2>3:
                    see_images1+=cc1
                    see_images2+=cc2
                    cc1=0
                    cc2=0
                    break
                if len(rd['face2l'])<1:
                    see_images2+=1
                    cc2=0
                    continue
                #检测到有两次比对，放弃此次比对结果
                #if len(rd['scorel'])>1:
                #    break
                #cc2+=1
                #compare_num+=1
                for score in rd['scorel']:
                       print "score:",score
                       score_ave+=score
                       compare_num+=1
                       cc2+=1
                       if score>score_threshold:
                           sameper_num+=1
                           break
                print "%d/%d"%(sameper_num,compare_num)
                if compare_num>max_compare_num:
                    break
                    #print ldmer.has_same_person(img1,img2) 
                    #print rd 
                cc2+=1
        score_ave=score_ave/(float(compare_num)+0.0000001)
        t2=tm.time()
        return float(sameper_num)/(float(compare_num)+0.0000001),score_ave,compare_num,imagedir1.split('/')[-1],imagedir2.split('/')[-1],t2-t1,"http://clt.management.vipkid.com.cn/operation/classroom/classroom/"
    def compare2dir(self,imagedir1,imagedir2,max_compare_num=30,score_threshold=0.8):
        timecost=0
        cc1=0
        cc2=0
        compare_num=0.0
        sameper_num=0.0
        score_ave=0.0
        max_see_images=50
        see_images1=0
        see_images2=0
        #print imagedir1
        #print os.listdir('/') 
        t1=tm.time()
        for imf1 in os.listdir(str(imagedir1)):
            #print imf1
            img1=cv2.imread(os.path.join(imagedir1,imf1))
            cc1+=1
            if compare_num>max_compare_num or see_images1>max_see_images or see_images2>max_see_images:
                break
            for imf2 in os.listdir(imagedir2):
                print cc1,cc2,compare_num,see_images1,see_images2,imf1,imf2
                img2=cv2.imread(os.path.join(imagedir2,imf2))
                rd=self.face_rec(img1,img2,0.0)
                print rd
                if compare_num>max_compare_num or see_images1>max_see_images or see_images2>max_see_images:
                    break
                if len(rd['face1l'])<1 or cc1>3 or cc2>3:
                    see_images1+=cc1
                    see_images2+=cc2
                    cc1=0
                    cc2=0
                    break
                if len(rd['face2l'])<1:
                    see_images2+=1
                    cc2=0
                    continue
                #检测到有两次比对，放弃此次比对结果
                #if len(rd['scorel'])>1:
                #    break
                #cc2+=1
                #compare_num+=1
                for score in rd['scorel']:
                       print "score:",score
                       score_ave+=score
                       compare_num+=1
                       cc2+=1
                       if score>score_threshold:
                           sameper_num+=1
                           break
                print "%d/%d"%(sameper_num,compare_num)
                if compare_num>max_compare_num:
                    break
                    #print ldmer.has_same_person(img1,img2) 
                    #print rd 
                cc2+=1
        score_ave=score_ave/(float(compare_num)+0.0000001)
        t2=tm.time()
        return float(sameper_num)/(float(compare_num)+0.0000001),score_ave,compare_num,imagedir1.split('/')[-1],imagedir2.split('/')[-1],t2-t1,"http://clt.management.vipkid.com.cn/operation/classroom/classroom/"

    def roc(self,mscore,outlier=-2):
        # outlier is the value that not to create the roc
        pos,neg=0,0
        db=[] 
        #for i in range(0,len(label)):
        for i in range(0,mscore.shape[0]):
            for j in range(0,mscore.shape[1]):
                #    print i
                tmp0=0
                tmp1=1
                if i==j:
                    tmp0=1
                    tmp1=0
                if mscore[i][j]!=outlier:
                    pos += tmp0
                    neg += tmp1
                    db.append([mscore[i][j],tmp0,tmp1])
                #print db[-1],pos,neg,label[i]
        db = sorted(db , key = lambda x:x[0] , reverse = True) #down sort
        
        #calculate ROC poistion
        xy_arr = []
        xy_arr_key = []
        error_equl_pos = []
        tp , fp = 0. , 0.
        for i in range(len(db)):
            tp += db[i][1]
            fp += db[i][2]
            xy_arr.append([fp/neg , tp/pos,db[i][0],fp/neg+tp/pos])
        
        
        #calculate the area under the curve: AUC
        auc = 0.
        prev_x = 0
        ic=0
        keypoint=[0.2,0.1,0.01,0.001]
        i=0
        for x ,y,score,sumxy in xy_arr:
            if x != prev_x:
                auc += (x - prev_x) * y
                prev_x = x
            if ic>0 and xy_arr[ic-1][1]<1-keypoint[i] and y>=1-keypoint[i]:
                xy_arr_key.append([x,y,score])
                if i<len(keypoint)-1:
                    i+=1
            if ic>0 and xy_arr[ic-1][3]<1 and sumxy>=1:
                error_equl_pos.append([x,y,score,sumxy])
            ic+=1
        print "the auc is %s."%auc
        x = [_v[0] for _v in xy_arr]
        y = [_v[1] for _v in xy_arr]
        print 'roc data is :'
        print xy_arr_key
        print 'error_equl_pos:'
        print error_equl_pos
        return xy_arr,xy_arr_key,error_equl_pos,auc
        #title="ROC curve of %s (AUC = %.4f)" % ('race_classier' , auc)
        #draw_curve(x,y,800,600,title,"False Positive Rate(FA)","True Positive Rate(RECALL)")




























        

 
