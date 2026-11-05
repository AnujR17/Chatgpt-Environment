import math
from checkpoint.face_mapping import movement_parameters,movement_label
from checkpoint.blob import parameters,movement_visual,follow_visual


def test_small_smile_survives_rest_deadzone():
    movement=movement_parameters({'mouthSmileLeft':.12,'mouthSmileRight':.12})
    assert movement_label(movement)==('happiness','Smile movement')
    assert movement['smile']>.3
    assert movement_parameters({'mouthSmileLeft':.02,'mouthSmileRight':.02})['smile']==0


def test_open_smile_has_laugh_animation_but_talking_alone_does_not():
    laugh=movement_parameters({'mouthSmileLeft':.35,'mouthSmileRight':.35,'jawOpen':.3,'eyeSquintLeft':.4,'eyeSquintRight':.4})
    assert movement_label(laugh)==('happiness','Open smile') and laugh['laugh']>.7 and laugh['eyes']<.9
    talking=movement_parameters({'jawOpen':.3})
    assert movement_label(talking)==('surprise','Mouth open') and talking['laugh']==0


def test_drawn_brows_are_not_erased_by_inner_brow_raise_or_need_a_frown():
    movement=movement_parameters({'browDownLeft':.12,'browDownRight':.12,'browInnerUp':.18,'mouthPressLeft':.2,'mouthPressRight':.2})
    assert movement_label(movement)==('anger','Brows drawn')
    visual=movement_visual(movement)
    assert visual['brow']>0 and visual['smile']<0 and visual['eyes']<1


def test_smiling_with_squinted_brows_stays_a_smile_and_rest_is_flat():
    movement=movement_parameters({'mouthSmileLeft':.3,'mouthSmileRight':.3,'browDownLeft':.3,'browDownRight':.3})
    assert movement_label(movement)[0]=='happiness'
    neutral=movement_parameters({'eyeBlinkLeft':.8,'eyeBlinkRight':.8})
    assert movement_label(neutral)[0]=='neutral' and neutral['smile']==neutral['jaw']==neutral['laugh']==0


def test_continuous_camera_targets_catch_up_without_restarting_a_long_ease():
    current=parameters(None);target=movement_visual({'smile':.8,'brow':0,'eyes':.8,'jaw':.4,'tension':0,'laugh':.5})
    for i in range(20):
        # New slightly changing targets at the camera's 4Hz cadence.
        target['smile']=.8+.01*math.sin(i)
        current=follow_visual(current,target,.25)
    assert current['smile']>.78 and current['jaw']>.39
    for _ in range(8):current=follow_visual(current,parameters(None),.1)
    assert abs(current['smile'])<.04 and current['laugh']<.03
