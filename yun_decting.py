import cv2
import numpy as np
class dectect:
    def __init__(self,frame,cb,alpha,area):
        self.frame = frame
        self.cb = cb
        self.alpha = alpha
        self.area = area
        self.gray_frame =  cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY)
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.fgmask = self.fgbg.apply(self.gray_frame)
    
    def make(self):
        self.gray_frame = cv2.cvtColor( self.frame , cv2.COLOR_BGR2GRAY)
        self.fgmask = self.fgbg.apply(self.gray_frame)
        self.ap = self.fgmask.copy()
        self.ap[self.ap>=100]=255
        self.ap[self.ap<=100]=0
        self.ap= cv2.medianBlur(self.ap,3)
        
        self.mp = abs(self.cb*1.0-self.gray_frame*1.0)
        self.mp = np.uint8(self.mp)
        self.histograme = cv2.calcHist([self.mp], [0], None, [256], [0, 256])
        self.histograme = np.reshape(self.histograme,256)
        self.th =  self.otus()
        self.mp [self.mp >= self.th] = 255
        self.mp [self.mp < self.th] = 0
        self.mp = np.uint8(self.mp)
        
        self.cb = (1.0-self.alpha)*self.cb + self.alpha*self.gray_frame
        
        self.combine = (self.ap*1.0+self.mp*1.0)
        self.combine[self.combine<=100]=0
        self.combine[self.combine>100]=255
        
        self.combine = np.uint8(self.combine)
        kernel = np.array(([[1,1,1],[1,1,1],[1,1,1]]), np.uint8)
        self.erodecombine = cv2.erode(self.combine, kernel, iterations=2)
        self.dilatecombine = cv2.dilate(self.erodecombine, kernel, iterations=5)
        self.combine_renoise= cv2.medianBlur(self.dilatecombine,5)
        
        #self.components_count,self.components=cv2.connectedComponents(self.combine_renoise)
        
        self.ComponentStats = cv2.connectedComponentsWithStats(self.combine_renoise, 4, cv2.CV_32S)
        
        self.component_result=self.frame.copy()
        self.components_mask=self.ComponentStats[1].copy()
        self.components_mask[self.components_mask>0]=255
        self.components_mask = np.uint8(self.components_mask)
        self.component_result[:,:,1]=self.components_mask
        
        
        
        self.rect_result=self.frame.copy()
        
        #self.component_work()
        for i in range (1,self.ComponentStats[0]):
            if self.ComponentStats[2][i,4] > self.area:
                left=self.ComponentStats[2][i,0]
                top=self.ComponentStats[2][i,1]
                width=self.ComponentStats[2][i,2]
                height=self.ComponentStats[2][i,3]
                cv2.rectangle(self.rect_result,(left,top),(left+width,top+height),(0,0,255),2)
                
    
    def otus(self):
        histo = np.reshape(self.histograme,256)
        total = histo.sum()
        sumB=0
        wB=0
        maximum = 0.0
    
        sum1 = np.dot(np.arange(256),histo)
        
        for i in range (0,256):
            wB = wB + histo[i]
            wF = total - wB
            if (wB == 0 or wF == 0):
                continue
            sumB = sumB + i * histo[i]
            mF = (sum1 - sumB) / wF
            between = wB * wF * ((sumB / wB) - mF) * ((sumB / wB) - mF)
            if ( between >= maximum ):
                level = i
                maximum = between
        return level
    '''
    def component_work(self):
        self.fish_list = np.zeros((self.components_count,5),'int')
        self.fish_list[:,1] = 100000
        self.fish_list[:,2] = 100000
        self.fish_list[:,3] = -1
        self.fish_list[:,4] = -1
        for i in range (0,self.components.shape[0]):
            for j in range (0,self.components.shape[1]):
                index = self.components[i,j]
                self.fish_list[index,0]=self.fish_list[index,0]+1
                
                self.fish_list[index,1]=j if j<self.fish_list[index,1] else self.fish_list[index,1]
                self.fish_list[index,2]=i if i<self.fish_list[index,2] else self.fish_list[index,2]
                self.fish_list[index,3]=j if j>self.fish_list[index,3] else self.fish_list[index,3]
                self.fish_list[index,4]=i if i>self.fish_list[index,4] else self.fish_list[index,4]
                '''
                
        
        
            
    