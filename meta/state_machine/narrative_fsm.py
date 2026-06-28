from .narrative_state import NarrativePhase
from meta.contracts.event import Event

class NarrativeFSM:
    def __init__(self):
        self.current_phase = NarrativePhase.ACCUMULATION
        self.phases_log = []

    def on_event(self, event: Event):
        transitions = {
            NarrativePhase.ACCUMULATION: {
                'LiquiditySweep': NarrativePhase.SWEEP
            },
            NarrativePhase.SWEEP: {
                'MSS': NarrativePhase.REPRICING
            },
            NarrativePhase.REPRICING: {
                'FVG': NarrativePhase.DELIVERY
            },
            NarrativePhase.DELIVERY: {
                'Mitigation': NarrativePhase.MITIGATION
            },
            NarrativePhase.MITIGATION: {
                'MSS': NarrativePhase.CONTINUATION
            }
        }
        phase_trans = transitions.get(self.current_phase, {})
        next_phase = phase_trans.get(event.semantic_type)
        if next_phase:
            self.current_phase = next_phase
            self.phases_log.append((event.timestamp, next_phase))
            return True
        return False
