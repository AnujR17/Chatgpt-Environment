import unittest
from checkpoint.session import Session
from checkpoint.attempts import (guidance_mode, start_attempt, finish_attempt, active_attempt,
                                phone_attempt, attempt_summary, saved_lessons)


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.s = Session()

    def test_camera_and_unknown_do_not_supply_cma_or_start_help(self):
        self.s.cue = object()
        self.assertEqual(guidance_mode(self.s)[0], 'choice')
        self.assertIsNone(phone_attempt(self.s))
        self.assertEqual(self.s.attempts, [])

    def test_recent_cma_changes_help_but_not_technique(self):
        self.s.check_in('angry', -.7, .8)
        row = start_attempt(self.s, 'placement')
        self.assertEqual(row['mode'], 'brief')
        self.assertEqual(row['key'], 'placement')
        self.s.check_in('sad', -.7, -.8)
        self.assertEqual(active_attempt(self.s)['mode'], 'brief', 'In-flight cue must not flicker')
        finish_attempt(self.s, 'stuck')
        self.assertEqual(start_attempt(self.s, 'placement')['mode'], 'small')

    def test_stale_mixed_and_invalid_reports_are_not_current_cma(self):
        self.s.check_in('angry', -.7, .8)
        self.s.reports[-1]['elapsed_seconds'] = self.s.elapsed() - 301
        self.assertEqual(guidance_mode(self.s)[0], 'choice')
        self.s.check_in('mixed')
        self.assertEqual(guidance_mode(self.s)[0], 'choice')
        for bad in (float('nan'), float('inf'), True, -2):
            self.s.reports[-1].update(valence=bad, arousal=.8)
            self.assertEqual(guidance_mode(self.s)[0], 'choice')

    def test_no_duplicate_start_or_double_rating(self):
        self.assertIsNotNone(start_attempt(self.s, 'grip'))
        self.assertIsNone(start_attempt(self.s, 'orange'))
        self.assertFalse(finish_attempt(self.s, 'won'))
        self.assertTrue(finish_attempt(self.s, 'helped', 'shorter reach'))
        self.assertFalse(finish_attempt(self.s, 'helped'))
        self.assertEqual(attempt_summary(self.s)['helped'], 1)

    def test_finished_paused_other_games_cannot_start_or_export_cue(self):
        self.s.game = 'Other game'
        self.assertIsNone(start_attempt(self.s, 'grip'))
        self.s.game = 'Getting Over It'
        start_attempt(self.s, 'grip')
        self.s.take_break()
        self.assertIsNone(phone_attempt(self.s))
        self.assertIsNone(start_attempt(self.s, 'grip'))
        self.s.end()
        self.assertIsNone(phone_attempt(self.s))

    def test_recall_uses_only_explicit_helpful_notes_for_matching_section(self):
        start_attempt(self.s, 'grip')
        finish_attempt(self.s, 'helped', 'shorter reach')
        saved = self.s.summary()
        new = Session()
        self.assertEqual(saved_lessons([saved], new, 'grip')[0]['lesson'], 'shorter reach')
        self.assertEqual(saved_lessons([saved], new, 'orange'), [])
        self.assertEqual(new.attempts, [])
        start_attempt(new, 'grip')
        finish_attempt(new, 'stuck', 'not useful')
        self.assertEqual(len(saved_lessons([saved], new, 'grip')), 1)
        new.game = 'Other'
        self.assertEqual(saved_lessons([saved], new, 'grip'), [])

    def test_unrated_and_dismissed_are_not_helpful(self):
        start_attempt(self.s, 'grip')
        self.assertEqual(attempt_summary(self.s)['unrated'], 1)
        finish_attempt(self.s, 'dismissed')
        self.assertEqual(attempt_summary(self.s)['helped'], 0)
        self.assertEqual(attempt_summary(self.s)['unrated'], 0)
        self.assertEqual(self.s.reports, [])

    def test_before_and_after_are_separate_explicit_reports(self):
        self.s.check_in('frustrated', -.7, .8)
        row = start_attempt(self.s, 'grip')
        self.assertEqual(row['cma_before']['report_index'], 0)
        self.assertIsNone(row['cma_after'])
        self.s.check_in('calm', .4, -.5)
        finish_attempt(self.s, 'helped')
        self.assertEqual(row['cma_after']['report_index'], 1)
        self.assertEqual(len(self.s.reports), 2)
        other = start_attempt(self.s, 'orange')
        finish_attempt(self.s, 'stuck')
        self.assertIsNone(other['cma_after'])
