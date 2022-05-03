#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv


# In[2]:


cam = cv.VideoCapture(0)


# In[ ]:


result, image = cam.read()


# In[ ]:


if result:
    
    cv.imshow("cam_testing", image)
    cv.imwrite("cam_testing.png",image)
    
    cv.waitKey(0)
    cv.destroyWindow("cam_testing")
    
else:
    print("No image detected. Please try again.")


# In[4]:


from PIL import Image
import numpy as np


# In[2]:


img = Image.open('/home/chenzhenglab/cam_testing.png')


# In[11]:


data = np.asarray(img)
data_trim = data[85:370,105:520]
Image.fromarray(data_trim).save('testing_trim.png')


# In[ ]:




