"""
CogniESL Agency — Hub-and-Spoke model with 5 agents:
Orchestrator (pure router) + ESL Intake Agent + ESL Pedagogy Agent + Slides Agent + Docs Agent.
"""
import os
from dotenv import load_dotenv
from agents import set_tracing_disabled, set_tracing_export_api_key
from patches.patch_agency_swarm_dual_comms import apply_dual_comms_patch
from patches.patch_file_attachment_refs import apply_file_attachment_reference_patch
from patches.patch_ipython_interpreter_composio import apply_ipython_composio_context_patch
from patches.patch_utf8_file_reads import apply_utf8_file_read_patch

load_dotenv()

apply_utf8_file_read_patch()
apply_dual_comms_patch()
apply_file_attachment_reference_patch()
apply_ipython_composio_context_patch()

_tracing_key = os.getenv("OPENAI_API_KEY")
if _tracing_key:
    set_tracing_export_api_key(_tracing_key)
else:
    set_tracing_disabled(True)


def create_agency(load_threads_callback=None):
    from agency_swarm import Agency
    from agency_swarm.tools import Handoff, SendMessage

    from orchestrator import create_orchestrator
    from esl_intake_agent.esl_intake_agent import create_esl_intake_agent
    from esl_pedagogy_agent.esl_pedagogy_agent import create_esl_pedagogy_agent
    from slides_agent import create_slides_agent
    from docs_agent import create_docs_agent

    orchestrator = create_orchestrator()
    esl_intake_agent = create_esl_intake_agent()
    esl_pedagogy_agent = create_esl_pedagogy_agent()
    slides_agent = create_slides_agent()
    docs_agent = create_docs_agent()

    # Handoff flows: Linear pipeline + cross-agent transfers
    handoff_flows = [
        # Phase 1: Orchestrator -> ESL Intake Agent -> Orchestrator
        (orchestrator, esl_intake_agent, Handoff),
        (esl_intake_agent, orchestrator, Handoff),
        # Phase 2: Orchestrator -> ESL Pedagogy Agent -> Orchestrator
        (orchestrator, esl_pedagogy_agent, Handoff),
        (esl_pedagogy_agent, orchestrator, Handoff),
        # Production returns
        (slides_agent, orchestrator, Handoff),
        (docs_agent, orchestrator, Handoff),
        # Cross-agent transfers
        (esl_intake_agent, esl_pedagogy_agent, Handoff),
        (esl_pedagogy_agent, esl_intake_agent, Handoff),
        (slides_agent, docs_agent, Handoff),
        (docs_agent, slides_agent, Handoff),
        (esl_intake_agent, slides_agent, Handoff),
        (esl_intake_agent, docs_agent, Handoff),
        (esl_pedagogy_agent, slides_agent, Handoff),
        (esl_pedagogy_agent, docs_agent, Handoff),
    ]

    # SendMessage: Parallel production from Orchestrator
    send_message_flows = [
        (orchestrator, slides_agent, SendMessage),
        (orchestrator, docs_agent, SendMessage),
    ]

    agency = Agency(
        orchestrator, esl_intake_agent, esl_pedagogy_agent, slides_agent, docs_agent,
        communication_flows=handoff_flows + send_message_flows,
        name="CogniESL",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_threads_callback,
    )

    return agency


if __name__ == "__main__":
    agency = create_agency()
    agency.tui(show_reasoning=True, reload=False)
