import json
import pytest
from checkpoint.session import Session,History,FEELINGS


def test_expression_cue_never_sets_cma():
    s=Session(experimental_analysis=True);generation=s.start_capture("camera")
    assert s.receive_cue({"expression":"anger","confidence":.99},generation)
    assert s.report is None and s.affect[1:3]==("Not reported","Not reported")
    s.check_in("engaged");s.receive_cue({"expression":"anger"},generation)
    assert s.affect[0]=="Engaged"


def test_capture_pause_clears_cues_and_rejects_inflight_results():
    s=Session(experimental_analysis=True);generation=s.start_capture("camera")
    s.receive_cue("test cue",generation);s.stop_capture()
    assert s.cue is None and not s.camera_active
    assert not s.receive_cue("late cue",generation)


def test_manual_checkin_and_break_never_resume_capture():
    s=Session();s.check_in("tense");s.take_break(now=100)
    assert s.break_deadline==130 and s.report=="tense" and not s.camera_active
    s.finish_break()
    assert not s.camera_active and s.report=="tense"


def test_checkins_need_neither_camera_nor_classifier():
    for key in FEELINGS:
        s=Session();s.check_in(key)
        assert s.report==key and not s.camera_active
        assert s.reports[-1]["source"]=="player_report"


def test_ended_session_rejects_capture_and_updates():
    s=Session();s.end()
    with pytest.raises(ValueError):s.start_capture("camera")
    with pytest.raises(ValueError):s.check_in("engaged")
    with pytest.raises(ValueError):s.take_break()


def test_history_requires_explicit_opt_in_and_contains_no_raw_media(tmp_path):
    h=History(tmp_path);s=Session();s.check_in("mixed");s.end()
    assert not h.save(s.summary()) and not h.path.exists()
    assert h.save(s.summary(),consent=True)
    text=h.path.read_text();records=json.loads(text)
    assert records[0]["check_ins"][0]["feeling"]=="mixed"
    assert not any(key in text for key in ["probabilities","face_box","frame","pixels",".mp4"])
    h.delete();assert not h.path.exists()


def test_model_cues_require_opt_in():
    s=Session();generation=s.start_capture("video")
    assert not s.receive_cue("anything",generation)


def test_corrupt_history_is_reported_not_overwritten(tmp_path):
    h=History(tmp_path);h.path.write_text("invalid json")
    with pytest.raises(json.JSONDecodeError):h.save({},consent=True)
    assert h.path.read_text()=="invalid json"
