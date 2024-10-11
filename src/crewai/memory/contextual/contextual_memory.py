from typing import Optional

from crewai.memory import EntityMemory, LongTermMemory, ShortTermMemory, UserMemory


class ContextualMemory:
    def __init__(
        self,
        stm: ShortTermMemory,
        ltm: LongTermMemory,
        em: EntityMemory,
        um: UserMemory,
        memory_provider: Optional[str] = None,  # Default value added
    ):
        self.stm = stm
        self.ltm = ltm
        self.em = em
        self.um = um
        self.memory_provider = memory_provider

    def build_context_for_task(self, task, context) -> str:
        """
        Automatically builds a minimal, highly relevant set of contextual information
        for a given task.
        """
        query = f"{task.description} {context}".strip()

        if query == "":
            return ""

        context = []
        context.append(self._fetch_ltm_context(task.description))
        context.append(self._fetch_stm_context(query))
        context.append(self._fetch_entity_context(query))
        if self.memory_provider == "mem0":
            context.append(self._fetch_user_memories(query))
        return "\n".join(filter(None, context))

    def _fetch_stm_context(self, query) -> str:
        """
        Fetches recent relevant insights from STM related to the task's description and expected_output,
        formatted as bullet points.
        """
        stm_results = self.stm.search(query)
        formatted_results = "\n".join([f"- {result}" for result in stm_results])
        return f"Recent Insights:\n{formatted_results}" if stm_results else ""

    def _fetch_ltm_context(self, task) -> Optional[str]:
        """
        Fetches historical data or insights from LTM that are relevant to the task's description and expected_output,
        formatted as bullet points.
        """
        ltm_results = self.ltm.search(task, latest_n=2)
        if not ltm_results:
            return None

        formatted_results = [
            suggestion
            for result in ltm_results
            for suggestion in result["metadata"]["suggestions"]  # type: ignore # Invalid index type "str" for "str"; expected type "SupportsIndex | slice"
        ]
        formatted_results = list(dict.fromkeys(formatted_results))
        formatted_results = "\n".join([f"- {result}" for result in formatted_results])  # type: ignore # Incompatible types in assignment (expression has type "str", variable has type "list[str]")

        return f"Historical Data:\n{formatted_results}" if ltm_results else ""

    def _fetch_entity_context(self, query) -> str:
        """
        Fetches relevant entity information from Entity Memory related to the task's description and expected_output,
        formatted as bullet points.
        """
        em_results = self.em.search(query)
        formatted_results = "\n".join(
            [
                f"- {result['memory'] if self.memory_provider == 'mem0' else result['context']}"
                for result in em_results
            ]  # type: ignore #  Invalid index type "str" for "str"; expected type "SupportsIndex | slice"
        )
        return f"Entities:\n{formatted_results}" if em_results else ""

    def _fetch_user_memories(self, query) -> str:
        """
        Fetches relevant user memory information from User Memory related to the task's description and expected_output,
        """
        print("query", query)
        um_results = self.um.search(query)
        print("um_results", um_results)
        formatted_results = "\n".join(
            [f"- {result['memory']}" for result in um_results]
        )
        print(f"User memories/preferences:\n{formatted_results}")
        return f"User memories/preferences:\n{formatted_results}" if um_results else ""
