import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
)


class AgentMessageLogger:
    """Structured logger for agent communication with rich formatting and context."""

    def __init__(self, name: str, log_level: int = logging.INFO):
        """Initialize the logger.

        Args:
            name: Name of the logger
            log_level: Logging level (default: logging.INFO)
        """
        self.name = name
        self.logger = logging.getLogger(f"agent_comm.{name}")
        self.logger.setLevel(log_level)

        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _get_message_type(self, message: BaseMessage) -> str:
        """Determine the type of the message."""
        if isinstance(message, HumanMessage):
            return "Human"
        elif isinstance(message, AIMessage):
            return "AI"
        elif isinstance(message, ToolMessage):
            return "Tool"
        elif isinstance(message, SystemMessage):
            return "System"
        return "Unknown"

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata for logging."""
        if not metadata:
            return ""
        return "\n" + "\n".join(f"    {k}: {v}" for k, v in metadata.items())

    def _format_tool_calls(self, message: AIMessage) -> str:
        """Format tool calls for logging."""
        if not hasattr(message, "tool_calls") or not message.tool_calls:
            return ""

        tool_calls = []
        for i, call in enumerate(message.tool_calls, 1):
            tool_call = f"  Tool Call {i}: {call.get('name', 'unknown')}\n"
            if "args" in call:
                tool_call += f"    Args: {json.dumps(call['args'], indent=4)}\n"
            if "id" in call:
                tool_call += f"    ID: {call['id']}\n"
            tool_calls.append(tool_call)

        return "\n" + "\n".join(tool_calls)

    def log_message(self, message: BaseMessage, direction: str = "-") -> None:
        """Log a message with structured formatting.

        Args:
            message: The message to log
            direction: Message direction ('->' for outgoing, '<-' for incoming, '-' for unknown)
        """
        try:
            msg_type = self._get_message_type(message)

            # Get basic message info
            log_parts = [
                f"[{msg_type} Message] {direction}",
                f"ID: {getattr(message, 'id', 'N/A')}",
            ]

            # Add content if present
            if hasattr(message, "content") and message.content:
                content = str(message.content).strip()
                if content:
                    log_parts.append(f"Content: {content}")

            # Add tool calls for AI messages
            if (
                msg_type == "AI"
                and hasattr(message, "tool_calls")
                and message.tool_calls
            ):
                tool_calls = self._format_tool_calls(message)
                if tool_calls:
                    log_parts.append(f"Tool Calls:{tool_calls}")

            # Add metadata if present
            metadata = getattr(message, "metadata", {})
            if metadata:
                log_parts.append(f"Metadata: {self._format_metadata(metadata)}")

            # Add response metadata if present
            response_metadata = getattr(message, "response_metadata", {})
            if response_metadata:
                log_parts.append(
                    f"Response Metadata: {self._format_metadata(response_metadata)}"
                )

            # Log the formatted message
            self.logger.info("\n" + "\n".join(log_parts) + "\n" + "-" * 80)

        except Exception as e:
            self.logger.error(f"Error logging message: {str(e)}\n{str(message)}")

    def log_agent_interaction(
        self,
        from_agent: str,
        to_agent: str,
        message: BaseMessage,
        is_response: bool = False,
    ) -> None:
        """Log an interaction between two agents.

        Args:
            from_agent: Name of the agent sending the message
            to_agent: Name of the agent receiving the message
            message: The message being sent
            is_response: Whether this is a response to a previous message
        """
        direction = "<-" if is_response else "->"
        self.logger.info(f"\n{'='*40} AGENT INTERACTION {'='*40}")
        self.logger.info(f"{from_agent} {direction} {to_agent}")
        self.log_message(message, direction)


class LangGraphLogger:
    """Logger for LangGraph agent communication."""

    def __init__(self, name: str, log_level: int = logging.INFO):
        """Initialize the logger.

        Args:
            name: Name of the logger
            log_level: Logging level (default: logging.INFO)
        """
        self.name = name
        self.logger = AgentMessageLogger(name, log_level)
        self.conversation_context = {
            "start_time": datetime.now().isoformat(),
            "message_count": 0,
            "last_sender": None,
        }

    def __call__(self, message: BaseMessage) -> None:
        """Log a message with context-aware formatting.

        Args:
            message: The message to log
        """
        try:
            self.conversation_context["message_count"] += 1

            # Extract metadata
            metadata = getattr(message, "metadata", {})
            agent_name = metadata.get("agent_name", "unknown")
            is_input = metadata.get("input", False)

            # Determine direction and log appropriately
            if is_input:
                self.logger.log_message(message, "<-")
            else:
                self.logger.log_message(message, "->")

            # Update last sender
            self.conversation_context["last_sender"] = agent_name

        except Exception as e:
            self.logger.logger.error(f"Error in LangGraphLogger: {str(e)}")
