# ODE-lateral-stability

This repo contains code for our MAT292 Final Project. We created a simulation to help analyze lateral stability in an aircraft. 

(copy paste shortened version of our intro here)


<!--                                                                                          
                                 zzyumhddehmsxzz                                         
                                zvh8YSRUYXVY500kx                                        
                               xg5TXkwyzzzzywm087nz   zzz                                
                             zpbVTly          xg1Xmzwh3Xnqnju                            
                             oaUUtz        zwsofYOXVLGFNZ8hsvz                           
                         wponcZPn       yri9VLHHIMOOPPNKIHIKP2kz                         
                         yvh99UVz      yqhszwj1SUUUTSQQPNLKIJJK6y                        
                            b0V1z      vmtxhYUUUUUTTSRPOONMKJIIK5z                       
                            daYX       yxzkUSTTTTTSRRPPNNMLKJIHINlzz                     
                            da1Uy zzz   zygPRRRSRRQQPONLKJJJIHHHIVwz                     
                            da3Vnztqv    zjQOPPPPPOOONMKJIIIIHHHHJVw                     
                           zea07914uyz    waOONNNNMMLLKJIHIIIHHHHHIM6y                   
                            h0a9W8y       zs8QQNLLLLKKJJIIHHIIHHHHHIWx                   
                            m9a6Uj        wcTRQPMKKKJJJIIIIHGGIIIIIUoz                   
                           zu7a7V7z       q3QPONNLJIIIIIIIIIHHGGGHK5vz                   
                            za9a1Wm       oZQQPONNMLJIHHIIIJJIIHHHHPgz                   
                             l6a6WZw    zs7SSRQPPONMKJIIJIJJJJQUX4gw                     
                             y5891Ubz     zunjicTJJKNOPONMKIN5y                          
                     zyxxyzz zh496XVk           zwngca90agpz                             
                 zzxodpyxk4hyzx2683TXuz                                                  
                 zma90agvzzx8Xoe407XS4x                                                  
                 m8568abclyzztZUT33XTT0z                  zz                             
                xg32224654fx zyfSUYWUSWj              zzhQZz                             
                xf22ZXWWVUVsz   iTVWUSR3s             zpOKLp                             
                zl41ZWUTSSSqz   y0SUTSSTaz            z8MKKSvz                           
                 yi1ZXUSSSZv    zsXSSSSR1rz           z6MKKLVt                           
                  zl1XVSSVny     xdSSSSRVhz           zgOLLMMPgwz                        
                    h2VSWoz      zpTSSSRSbz           zyYNNNNNNO3luwxyzzz                
                    o7Zbwz       zsVSSSRS0y             y3QOOPPPPPPPPPTaw                
                   zqpwz         zqUSSSRSaz              zxm5SOOPPPWctyz                 
                                zykUTSSRUdz                  zyxxxyz                     
                                 zxuuuuuux                                                -->




## Installation

Our code is written in Python3. To reproduce our results, start by installing the dependencies.

1. Clone this repository
2. Create and activate virtual environment in Python
3. Install the dependendencies: `pip install pyglet numpy pynput matplotlib sympy`

To run the sim, run `python vis.py` in your terminal. A GUI will pop up showing the aircraft motion. Close the sim by closing the GUI. This generates a file called `data-SIM_START_DATE_AND_TIME.txt` in the folder `./data/`. This file is formatted as:

```
horizontal position (m)     vertical position (m)     bank angle (deg)    time (s)
```

To plot this data, run `python grapher.py`.  

