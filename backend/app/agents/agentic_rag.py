"""
Agentic RAG
Autonomous agent with tools for document analysis
"""
import logging
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from datetime import datetime

from app.services.rag_service import get_rag_service
from app.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


class AgentState(str, Enum):
    """Agent task states"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Tool:
    """Agent tool definition"""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Dict[str, Any]
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters
    
    async def execute(self, **kwargs) -> Any:
        """Execute tool"""
        return await self.func(**kwargs)


class AgentTask:
    """Agent task execution"""
    
    def __init__(
        self,
        task_id: str,
        name: str,
        description: str,
        instructions: str,
        user_id: str,
        documents: Optional[List[str]] = None
    ):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.instructions = instructions
        self.user_id = user_id
        self.documents = documents or []
        
        self.state = AgentState.INITIALIZED
        self.start_time = None
        self.end_time = None
        self.iterations = 0
        self.result = None
        self.error = None
        self.status_message = "Task initialized"
    
    def start(self) -> None:
        """Start task execution"""
        self.state = AgentState.RUNNING
        self.start_time = datetime.utcnow()
        self.status_message = "Task execution started"
        logger.info(f"Task {self.task_id} started")
    
    def complete(self, result: Any) -> None:
        """Complete task execution"""
        self.state = AgentState.COMPLETED
        self.end_time = datetime.utcnow()
        self.result = result
        self.status_message = "Task completed successfully"
        logger.info(f"Task {self.task_id} completed")
    
    def fail(self, error: Exception) -> None:
        """Mark task as failed"""
        self.state = AgentState.FAILED
        self.end_time = datetime.utcnow()
        self.error = str(error)
        self.status_message = f"Task failed: {str(error)}"
        logger.error(f"Task {self.task_id} failed: {error}")
    
    def cancel(self) -> None:
        """Cancel task execution"""
        self.state = AgentState.CANCELLED
        self.end_time = datetime.utcnow()
        self.status_message = "Task cancelled"
        logger.info(f"Task {self.task_id} cancelled")
    
    def get_execution_time(self) -> float:
        """Get execution time in seconds"""
        if not self.start_time:
            return 0.0
        
        end = self.end_time or datetime.utcnow()
        return (end - self.start_time).total_seconds()


class AgenticRAG:
    """
    Agentic RAG system
    Autonomous agent for document analysis and task execution
    """
    
    def __init__(self, user_id: str):
        """Initialize agentic RAG"""
        self.user_id = user_id
        self.tools = self._initialize_tools()
        self.tasks: Dict[str, AgentTask] = {}
        logger.info(f"Agentic RAG initialized for user {user_id}")
    
    def _initialize_tools(self) -> Dict[str, Tool]:
        """Initialize available tools"""
        tools = {
            "analyze_query": Tool(
                name="analyze_query",
                description="Analyze and break down the query",
                func=self._analyze_query,
                parameters={"query": "str"}
            ),
            "retrieve_documents": Tool(
                name="retrieve_documents",
                description="Retrieve relevant documents",
                func=self._retrieve_documents,
                parameters={"query": "str", "top_k": "int"}
            ),
            "generate_summary": Tool(
                name="generate_summary",
                description="Generate summary of documents",
                func=self._generate_summary,
                parameters={"documents": "List[str]"}
            ),
            "extract_insights": Tool(
                name="extract_insights",
                description="Extract key insights from documents",
                func=self._extract_insights,
                parameters={"documents": "List[str]"}
            ),
        }
        return tools
    
    async def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze user query"""
        llm = get_llm_service()
        if not llm:
            return {"analysis": "LLM service not available"}

        prompt = f"""Analyze the following query and break it down into key components:

Query: {query}

Analysis:"""

        analysis = llm.generate(prompt, temperature=0.5)
        return {"analysis": analysis}
    
    async def _retrieve_documents(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents"""
        rag = get_rag_service()
        if not rag:
            return []

        return rag.query_documents(
            query=query,
            user_id=self.user_id,
            top_k=top_k
        )
    
    async def _generate_summary(self, documents: List[str]) -> str:
        """Generate summary of documents"""
        llm = get_llm_service()
        if not llm:
            return "LLM service not available"

        combined_text = "\n\n".join(documents)
        return llm.summarize(combined_text)
    
    async def _extract_insights(self, documents: List[str]) -> Dict[str, Any]:
        """Extract key insights from documents"""
        llm = get_llm_service()
        if not llm:
            return {}

        combined_text = "\n\n".join(documents)

        prompt = f"""Extract 3-5 key insights from the following documents:

{combined_text}

Key Insights:"""

        insights = llm.generate(prompt, temperature=0.5)
        return {"insights": insights}
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute an agent task
        Autonomously processes documents and generates results
        """
        try:
            task.start()
            self.tasks[task.task_id] = task
            
            # Step 1: Analyze instructions
            logger.info(f"Analyzing instructions for task {task.task_id}")
            task.status_message = "Analyzing task instructions"
            
            # Step 2: Retrieve relevant documents
            logger.info(f"Retrieving documents for task {task.task_id}")
            task.status_message = "Retrieving relevant documents"
            task.iterations += 1
            
            docs = await self._retrieve_documents(
                query=task.instructions,
                top_k=10
            )
            
            # Step 3: Analyze documents
            logger.info(f"Analyzing documents for task {task.task_id}")
            task.status_message = "Analyzing documents"
            task.iterations += 1
            
            doc_contents = [doc["content"] for doc in docs]
            insights = await self._extract_insights(doc_contents)
            
            # Step 4: Generate result
            logger.info(f"Generating result for task {task.task_id}")
            task.status_message = "Generating task result"
            task.iterations += 1
            
            summary = await self._generate_summary(doc_contents)
            
            # Compile result
            result = {
                "task_name": task.name,
                "summary": summary,
                "insights": insights,
                "documents_analyzed": len(docs),
                "iterations": task.iterations
            }
            
            task.complete(result)
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            task.fail(e)
            raise
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        task = self.tasks.get(task_id)
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        return {
            "task_id": task_id,
            "state": task.state.value,
            "status_message": task.status_message,
            "progress": min(100, (task.iterations * 20)),  # 5 steps = 100%
            "iterations": task.iterations,
            "execution_time": task.get_execution_time()
        }
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Get task result"""
        task = self.tasks.get(task_id)
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.state != AgentState.COMPLETED:
            raise ValueError(f"Task {task_id} not completed yet")
        
        return {
            "task_id": task_id,
            "result": task.result,
            "execution_time": task.get_execution_time(),
            "iterations": task.iterations
        }


# Global agent instances
agents: Dict[str, AgenticRAG] = {}


def get_agent(user_id: str) -> AgenticRAG:
    """Get or create agent for user"""
    if user_id not in agents:
        agents[user_id] = AgenticRAG(user_id)
    return agents[user_id]
