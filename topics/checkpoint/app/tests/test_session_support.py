"""Support choices are based on confirmed CMA, never camera estimates."""
import unittest
from checkpoint.session import Session
from checkpoint.support import SupportController, support_summary


class SupportPolicyTests(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.controller = SupportController()

    def test_unknown_and_positive_states_do_not_prompt(self):
        self.assertIsNone(self.controller.sync(self.session))
        self.session.check_in("excited", .7, .8)
        self.assertIsNone(self.controller.sync(self.session))
        self.session.check_in("calm", .6, -.6)
        self.assertIsNone(self.controller.sync(self.session))
        self.assertEqual(self.session.support_events, [])

    def test_negative_high_and_low_activation_have_different_choices(self):
        self.session.check_in("frustrated", -.7, .8)
        self.assertEqual(self.controller.sync(self.session).kind, "reset")
        self.session.check_in("sad", -.6, -.7)
        self.assertEqual(self.controller.sync(self.session).kind, "focus")

    def test_observed_face_cannot_create_a_support_offer_or_cma(self):
        from checkpoint.cues import Cue
        self.session.experimental_analysis = True
        generation = self.session.start_capture("camera")
        self.session.receive_cue(Cue("accepted", "anger", .99), generation)
        self.assertIsNone(self.controller.sync(self.session))
        self.assertIsNone(self.session.valence)
        self.assertEqual(len(self.session.reports), 0)

    def test_keep_going_silences_subsequent_reports_for_this_session(self):
        self.session.check_in("angry", -.7, .8)
        self.controller.sync(self.session)
        self.assertTrue(self.controller.keep_going(self.session))
        for _ in range(10):
            self.assertIsNone(self.controller.sync(self.session))
        self.session.check_in("frustrated", -.8, .9)
        self.assertIsNone(self.controller.sync(self.session))
        self.assertEqual(support_summary(self.session.support_events)["kept_playing"], 1)

    def test_new_session_restores_choice_without_carrying_suppression(self):
        self.session.check_in("angry", -.7, .8)
        self.controller.sync(self.session)
        self.controller.keep_going(self.session)
        new = Session(started=self.session.started + 1)
        new.check_in("frustrated", -.7, .8)
        self.assertEqual(self.controller.sync(new).kind, "reset")

    def test_reset_is_recorded_once_and_feedback_is_optional(self):
        self.session.check_in("frustrated", -.6, .8)
        self.controller.sync(self.session)
        self.session.take_break()
        first = self.controller.start_reset(self.session)
        self.assertEqual(first, self.controller.start_reset(self.session))
        self.assertIsNone(self.controller.sync(self.session))
        self.session.finish_break()
        self.controller.sync(self.session)
        self.assertEqual(self.controller.feedback_reset, first)
        self.assertTrue(self.controller.feedback(self.session, True))
        self.assertFalse(self.controller.feedback(self.session, False))
        summary = support_summary(self.session.support_events)
        self.assertEqual(summary["resets"], 1)
        self.assertEqual(summary["rated_helpful"], 1)
        self.assertEqual(summary["unrated_resets"], 0)
        self.assertFalse(self.session.camera_active)
        self.assertEqual(len(self.session.reports), 1)

    def test_skipped_feedback_and_accepted_reset_do_not_imply_benefit(self):
        self.session.take_break()
        self.controller.start_reset(self.session)
        self.session.finish_break()
        self.controller.sync(self.session)
        self.controller.feedback(self.session, None)
        summary = support_summary(self.session.support_events)
        self.assertEqual(summary["rated_helpful"], 0)
        self.assertEqual(summary["unrated_resets"], 1)
        self.assertEqual(len(self.session.reports), 0)

    def test_focus_cancellation_and_session_end_have_no_hidden_action(self):
        self.session.check_in("sad", -.7, -.8)
        self.controller.sync(self.session)
        self.assertFalse(self.controller.set_focus(self.session, "  "))
        self.assertEqual(self.session.support_events, [])
        self.assertTrue(self.controller.set_focus(self.session, "One slower attempt"))
        self.assertEqual(self.session.practice_goal, "One slower attempt")
        self.assertIsNone(self.controller.sync(self.session))
        self.session.end()
        self.assertIsNone(self.controller.sync(self.session))
        self.assertFalse(self.controller.keep_going(self.session))

    def test_not_sure_is_not_forced_into_a_cma_region(self):
        self.session.check_in("mixed")
        self.assertIsNone(self.controller.sync(self.session))
        self.assertIsNone(self.session.valence)
        self.assertIsNone(self.session.arousal)


if __name__ == "__main__":
    unittest.main()
