import os

from giga_agent.agents.experimental.module import ExperimentalModule
from giga_agent.core.agent.base import BaseAgent
from giga_agent.core.module import BaseModule
from giga_agent.memory.module import MemoryModule
from giga_agent.modules.analyze_images import AnalyzeImagesModule
from giga_agent.modules.auth.module import AuthModule
from giga_agent.modules.clarify import ClarifyModule
from giga_agent.modules.deep_research import DeepResearchModule
from giga_agent.modules.image import ImageModule
from giga_agent.modules.integrations.vk import VKModule
from giga_agent.modules.integrations.yandex_calendar.module import YandexCalendarModule
from giga_agent.modules.integrations.yandex_disk import YandexDiskModule
from giga_agent.modules.integrations.yandex_mail import YandexMailModule
from giga_agent.modules.io import IOModule
from giga_agent.modules.mcp import McpModule
from giga_agent.modules.projects import ProjectsModule
from giga_agent.modules.rag import RagModule
from giga_agent.modules.repl import ReplModule
from giga_agent.modules.scheduler.module import SchedulerModule
from giga_agent.modules.scraper import ScraperModule
from giga_agent.modules.search import SearchModule
from giga_agent.modules.skills.module import SkillsModule
from giga_agent.modules.subagents_legacy.module import SubAgentLegacyModule
from giga_agent.modules.weather import WeatherModule


_CORE_MODULES = {
    "auth": AuthModule,
    "clarify": ClarifyModule,
    "io": IOModule,
    "projects": ProjectsModule,
    "memory": MemoryModule,
}

_FEATURE_MODULES = {
    "repl": ReplModule,
    "image": ImageModule,
    "analyze_images": AnalyzeImagesModule,
    "scraper": ScraperModule,
    "search": SearchModule,
    "rag": RagModule,
    "skills": SkillsModule,
    "mcp": McpModule,
    "vk": VKModule,
    "yandex_disk": YandexDiskModule,
    "yandex_mail": YandexMailModule,
    "yandex_calendar": YandexCalendarModule,
    "weather": WeatherModule,
    "deep_research": DeepResearchModule,
    "scheduler": SchedulerModule,
    "subagents_legacy": SubAgentLegacyModule,
    "experimental": ExperimentalModule,
}



class GigaAgent(BaseAgent):
    def get_modules(self) -> list[BaseModule]:
        raw = os.getenv("GIGA_AGENT_FEATURES", "")  # напр. "core,legal_pipeline"
        enabled = {m.strip() for m in raw.split(",") if m.strip()}
        modules: list[BaseModule] = []
        # core всегда; feature-модули — только по флагу
        for key, cls in _CORE_MODULES.items():
            modules.append(cls())
        for key, cls in _FEATURE_MODULES.items():
            # if key in enabled:
            modules.append(cls())
        if "legal_pipeline" in enabled:
            from giga_agent.modules.legal_pipeline import LegalPipelineModule
            modules.append(LegalPipelineModule())
        return modules
