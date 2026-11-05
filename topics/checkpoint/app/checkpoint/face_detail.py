"""Geometric hand proximity and conservative visible-teeth cues, not emotion labels."""
import cv2
import numpy as np

INNER_LIPS=(78,191,80,81,82,13,312,311,310,415,308,324,318,402,317,14,87,178,88,95)


def mouth_polygon(points):return np.array([(points[i].x,points[i].y) for i in INNER_LIPS],dtype=np.float32)


def hand_mouth(landmarks,mouth):
    result={'near':False,'occluded':False,'side':1.}
    if mouth is None or not len(landmarks):return result
    mouth=np.asarray(mouth,dtype=np.float32);center=mouth.mean(0);width=max(.02,float(np.ptp(mouth[:,0])))
    area=max(1e-7,cv2.contourArea(cv2.convexHull(mouth)))
    for hand in landmarks:
        xy=np.array([(p.x,p.y) for p in hand],dtype=np.float32)
        tips=xy[[4,8,12,16,20]]
        distance=float(np.linalg.norm((tips-center)/np.array([width,width*.8]),axis=1).min())
        overlap,_=cv2.intersectConvexConvex(cv2.convexHull(mouth),cv2.convexHull(xy))
        if distance<.9 or overlap/area>.12:
            result={'near':True,'occluded':bool(overlap/area>.3),'side':-1. if xy.mean(0)[0]<center[0] else 1.}
            if result['occluded']:break
    return result


def visible_teeth(frame,points,occluded=False):
    """Bright low-chroma horizontal regions strictly inside the lip aperture.
    A conservative appearance heuristic: highlights/dentures can still confuse it.
    """
    if occluded:return 0.
    h,w=frame.shape[:2];poly=mouth_polygon(points)*np.array([w,h],np.float32)
    x,y,rw,rh=cv2.boundingRect(poly.astype(np.int32));x=max(0,x);y=max(0,y);rw=min(rw,w-x);rh=min(rh,h-y)
    if rw<12 or rh<3 or rh/rw<.035:return 0.
    crop=frame[y:y+rh,x:x+rw]
    if crop.size==0:return 0.
    mask=np.zeros((rh,rw),np.uint8);cv2.fillPoly(mask,[(poly-[x,y]).astype(np.int32)],255)
    hsv=cv2.cvtColor(crop,cv2.COLOR_BGR2HSV);gray=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY);inside=gray[mask>0]
    if not inside.size or np.percentile(inside,95)-np.percentile(inside,15)<28:return 0.
    threshold=max(135.,float(np.percentile(inside,40))+28)
    white=((gray>=threshold)&(hsv[:,:,1]<105)&(mask>0)).astype(np.uint8)
    count,_,stats,_=cv2.connectedComponentsWithStats(white,connectivity=8)
    strength=0.
    for left,top,width,height,area in stats[1:]:
        fraction=float(area)/max(1,int((mask>0).sum()))
        if width>=rw*.25 and width/max(1,height)>1.35 and .08<=fraction<=.94:
            strength=max(strength,min(1.,fraction*3))
    return strength
