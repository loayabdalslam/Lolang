#!/usr/bin/env python3
"""
Benchmark script for LOLANG AI Agent System.
Tests performance of AI agent, decryptor, and overall system.
"""
import asyncio
import time
import json
import statistics
import logging
from typing import Dict, List, Any
from dataclasses import dataclass, field
from terminal_colors import TerminalColors
from config import GeminiConfig
from ai_agent import AIAgent
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Stores benchmark execution results."""
    test_name: str
    total_time: float = 0.0
    avg_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    times: List[float] = field(default_factory=list)
    
    def add_result(self, time_taken: float, success: bool = True):
        """Add a single benchmark result."""
        self.times.append(time_taken)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.total_time += time_taken
        self.min_time = min(self.min_time, time_taken)
        self.max_time = max(self.max_time, time_taken)
        self.avg_time = statistics.mean(self.times) if self.times else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "test_name": self.test_name,
            "total_time": round(self.total_time, 3),
            "avg_time": round(self.avg_time, 3),
            "min_time": round(self.min_time, 3) if self.min_time != float('inf') else 0,
            "max_time": round(self.max_time, 3),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_requests": self.success_count + self.failure_count,
            "success_rate": f"{(self.success_count / max(1, self.success_count + self.failure_count)) * 100:.2f}%"
        }


class LolangBenchmark:
    """Benchmark suite for LOLANG system components."""
    
    # Sample messages for testing
    TEST_MESSAGES = [
        "Hello, how are you?",
        "What is artificial intelligence?",
        "Let's discuss machine learning",
        "Can you explain neural networks?",
        "What are the benefits of AI?",
    ]
    
    # Sample LOLANG messages for decryption testing
    SAMPLE_LOLANG_MESSAGES = [
        "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?",
        "⟦LO-2⟧ GREET: AI agent?",
        "⟦LO-2⟧ DISC: Topic=ML",
    ]
    
    def __init__(self, config: GeminiConfig = None, iterations: int = 3):
        """
        Initialize benchmark suite.
        
        Args:
            config: Gemini configuration
            iterations: Number of iterations per test
        """
        self.config = config or GeminiConfig.get_default_config()
        self.iterations = iterations
        self.visualizer = MessageVisualizer()
        self.results: List[BenchmarkResult] = []
        
        # Initialize components
        self.agent = AIAgent("Benchmark-Agent", TerminalColors.CYAN, self.config)
        self.decryptor = LolangDecryptor(self.config)
    
    def _run_timed_test(self, test_func, test_name: str, *args, **kwargs) -> BenchmarkResult:
        """
        Run a timed test and collect results.
        
        Args:
            test_func: Function to benchmark
            test_name: Name of the test
            *args, **kwargs: Arguments to pass to test function
            
        Returns:
            BenchmarkResult with collected metrics
        """
        result = BenchmarkResult(test_name=test_name)
        
        for i in range(self.iterations):
            start_time = time.time()
            try:
                test_func(*args, **kwargs)
                elapsed = time.time() - start_time
                result.add_result(elapsed, success=True)
                print(f"  ✓ Iteration {i+1}/{self.iterations}: {elapsed:.3f}s")
            except Exception as e:
                elapsed = time.time() - start_time
                result.add_result(elapsed, success=False)
                print(f"  ✗ Iteration {i+1}/{self.iterations}: {elapsed:.3f}s - {str(e)}")
        
        return result
    
    async def _run_async_timed_test(self, async_test_func, test_name: str, *args, **kwargs) -> BenchmarkResult:
        """
        Run an async timed test and collect results.
        
        Args:
            async_test_func: Async function to benchmark
            test_name: Name of the test
            *args, **kwargs: Arguments to pass to test function
            
        Returns:
            BenchmarkResult with collected metrics
        """
        result = BenchmarkResult(test_name=test_name)
        
        for i in range(self.iterations):
            start_time = time.time()
            try:
                await async_test_func(*args, **kwargs)
                elapsed = time.time() - start_time
                result.add_result(elapsed, success=True)
                print(f"  ✓ Iteration {i+1}/{self.iterations}: {elapsed:.3f}s")
            except Exception as e:
                elapsed = time.time() - start_time
                result.add_result(elapsed, success=False)
                print(f"  ✗ Iteration {i+1}/{self.iterations}: {elapsed:.3f}s - {str(e)}")
        
        return result
    
    def test_agent_chat(self):
        """Benchmark AI agent chat response time."""
        print(TerminalColors.format_header("AI Agent Chat Benchmark"))
        
        def chat_test(message):
            history = [{"role": "user", "content": message}]
            response = self.agent.chat(history)
            if not response or response.startswith("[Error"):
                raise Exception(response)
        
        for i, message in enumerate(self.TEST_MESSAGES[:2]):
            test_name = f"Agent Chat - Message {i+1}"
            result = self._run_timed_test(chat_test, test_name, message, iterations=1)
            self.results.append(result)
            print()
    
    async def test_decryptor_async(self):
        """Benchmark decryptor async decryption time."""
        print(TerminalColors.format_header("Decryptor Async Benchmark"))
        
        async def decrypt_test(message):
            result = await self.decryptor.decrypt(message)
            if not result or result.startswith("[Decryption failed"):
                raise Exception(result)
        
        for i, message in enumerate(self.SAMPLE_LOLANG_MESSAGES):
            test_name = f"Decrypt Async - Message {i+1}"
            result = await self._run_async_timed_test(decrypt_test, test_name, message, iterations=1)
            self.results.append(result)
            print()
    
    def test_decryptor_sync(self):
        """Benchmark decryptor sync decryption time."""
        print(TerminalColors.format_header("Decryptor Sync Benchmark"))
        
        def decrypt_test(message):
            result = self.decryptor.decrypt_sync(message)
            if not result or result.startswith("[Decryption failed"):
                raise Exception(result)
        
        for i, message in enumerate(self.SAMPLE_LOLANG_MESSAGES):
            test_name = f"Decrypt Sync - Message {i+1}"
            result = self._run_timed_test(decrypt_test, test_name, message, iterations=1)
            self.results.append(result)
            print()
    
    def test_visualizer(self):
        """Benchmark message visualization time."""
        print(TerminalColors.format_header("Message Visualizer Benchmark"))
        
        def visualize_test(role, message):
            result = self.visualizer.visualize_message(role, message)
            if not result:
                raise Exception("Visualization failed")
        
        for i, message in enumerate(self.TEST_MESSAGES[:3]):
            test_name = f"Visualization - Message {i+1}"
            result = self._run_timed_test(visualize_test, test_name, "Test-Agent", message)
            self.results.append(result)
            print()
    
    def test_config_validation(self):
        """Benchmark configuration validation time."""
        print(TerminalColors.format_header("Config Validation Benchmark"))
        
        def validate_test():
            result = self.config.validate()
            if not result:
                raise Exception("Validation failed")
        
        result = self._run_timed_test(validate_test, "Config Validation")
        self.results.append(result)
        print()
    
    def print_summary(self):
        """Print benchmark summary report."""
        print(TerminalColors.format_header("Benchmark Summary"))
        print()
        
        for result in self.results:
            data = result.to_dict()
            print(f"{TerminalColors.BOLD}{data['test_name']}{TerminalColors.RESET}")
            print(f"  Total Time: {data['total_time']}s")
            print(f"  Avg Time: {data['avg_time']}s")
            print(f"  Min Time: {data['min_time']}s")
            print(f"  Max Time: {data['max_time']}s")
            print(f"  Success: {data['success_count']}/{data['total_requests']} ({data['success_rate']})")
            print()
        
        # Overall statistics
        total_time = sum(r.total_time for r in self.results)
        total_success = sum(r.success_count for r in self.results)
        total_failures = sum(r.failure_count for r in self.results)
        total_tests = total_success + total_failures
        
        print(TerminalColors.format_separator('='))
        print(f"{TerminalColors.BOLD}Overall Results:{TerminalColors.RESET}")
        print(f"  Total Tests: {total_tests}")
        print(f"  Successful: {total_success}")
        print(f"  Failed: {total_failures}")
        print(f"  Total Time: {total_time:.3f}s")
        print(f"  Success Rate: {(total_success / max(1, total_tests)) * 100:.2f}%")
        print(TerminalColors.format_separator('='))
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """
        Save benchmark results to JSON file.
        
        Args:
            filename: Output filename
        """
        results_data = {
            "benchmark_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": {
                "model": self.config.model_name,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "iterations": self.iterations
            },
            "results": [r.to_dict() for r in self.results]
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\nResults saved to {filename}")
    
    async def run_all(self):
        """Run all benchmarks."""
        print(TerminalColors.format_header("LOLANG Benchmark Suite"))
        print(f"Model: {self.config.model_name}")
        print(f"Iterations: {self.iterations}")
        print(f"Temperature: {self.config.temperature}")
        print()
        
        # Run synchronous benchmarks
        self.test_config_validation()
        self.test_visualizer()
        self.test_agent_chat()
        self.test_decryptor_sync()
        
        # Run async benchmarks
        await self.test_decryptor_async()
        
        # Print summary
        self.print_summary()
        
        # Save results
        self.save_results()


async def main():
    """Main entry point."""
    logging.basicConfig(level=logging.WARNING)
    
    # Use test configuration with lower resource usage
    config = GeminiConfig.get_default_config()
    
    if not config.validate():
        print(TerminalColors.colorize(
            "ERROR: Invalid configuration. Please set GEMINI_API_KEY in .env file.",
            TerminalColors.RED
        ))
        return
    
    # Create benchmark with fewer iterations for faster testing
    benchmark = LolangBenchmark(config=config, iterations=2)
    
    try:
        await benchmark.run_all()
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\n\nBenchmark interrupted", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"\n\nBenchmark error: {e}", TerminalColors.RED))
        logger.error(f"Benchmark error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nBenchmark interrupted", TerminalColors.YELLOW))
