#!/usr/bin/env python3
"""
Benchmark script for LOLANG AI Agent System.
Tests performance on a dataset of 100 coding-related samples.
"""
import asyncio
import time
import json
import statistics
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from terminal_colors import TerminalColors
from config import GeminiConfig
from ai_agent import AIAgent
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

logger = logging.getLogger(__name__)


# ============================================================================
# CODING DATASET - 100 Samples
# ============================================================================

CODING_DATASET = [
    # Python Programming (1-20)
    {"category": "Python", "message": "Write a Python function to reverse a string", "difficulty": "easy"},
    {"category": "Python", "message": "Create a binary search algorithm in Python", "difficulty": "medium"},
    {"category": "Python", "message": "Implement a decorator that measures function execution time", "difficulty": "medium"},
    {"category": "Python", "message": "Write a list comprehension to filter even numbers", "difficulty": "easy"},
    {"category": "Python", "message": "Create a class for a stack data structure", "difficulty": "medium"},
    {"category": "Python", "message": "Write code to read and parse a JSON file", "difficulty": "easy"},
    {"category": "Python", "message": "Implement merge sort algorithm", "difficulty": "hard"},
    {"category": "Python", "message": "Create a generator that yields Fibonacci numbers", "difficulty": "medium"},
    {"category": "Python", "message": "Write a context manager for database connection", "difficulty": "hard"},
    {"category": "Python", "message": "Implement a simple HTTP server using sockets", "difficulty": "hard"},
    {"category": "Python", "message": "Write code to flatten a nested dictionary", "difficulty": "medium"},
    {"category": "Python", "message": "Create a thread pool executor example", "difficulty": "medium"},
    {"category": "Python", "message": "Write a regex pattern to validate email addresses", "difficulty": "easy"},
    {"category": "Python", "message": "Implement a singleton pattern in Python", "difficulty": "medium"},
    {"category": "Python", "message": "Create a simple web scraper using BeautifulSoup", "difficulty": "medium"},
    {"category": "Python", "message": "Write code to merge two sorted lists", "difficulty": "easy"},
    {"category": "Python", "message": "Implement a LRU cache from scratch", "difficulty": "hard"},
    {"category": "Python", "message": "Create a custom exception hierarchy", "difficulty": "easy"},
    {"category": "Python", "message": "Write async code to fetch data from multiple URLs", "difficulty": "hard"},
    {"category": "Python", "message": "Implement a simple blockchain class", "difficulty": "hard"},
    
    # JavaScript/TypeScript (21-40)
    {"category": "JavaScript", "message": "Write a JavaScript function to debounce user input", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Create a promise that retries on failure", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Implement array map function from scratch", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Write code to deep clone an object", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Create a simple event emitter class", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Implement a throttle function for scroll events", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Write async/await code to fetch API data", "difficulty": "easy"},
    {"category": "JavaScript", "message": "Create a middleware pattern like Express", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Implement a simple state management system", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Write code to validate a form with regex", "difficulty": "easy"},
    {"category": "JavaScript", "message": "Create a curry function that handles multiple args", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Implement a pub/sub pattern from scratch", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Write a function to flatten nested arrays", "difficulty": "easy"},
    {"category": "JavaScript", "message": "Create a simple router implementation", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Implement lazy loading for images", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Write code to implement drag and drop", "difficulty": "medium"},
    {"category": "JavaScript", "message": "Create a simple virtual DOM implementation", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Implement a memoization utility function", "difficulty": "easy"},
    {"category": "JavaScript", "message": "Write TypeScript generics for a generic repository", "difficulty": "hard"},
    {"category": "JavaScript", "message": "Create a simple WebSocket client wrapper", "difficulty": "medium"},
    
    # Algorithms & Data Structures (41-60)
    {"category": "Algorithms", "message": "Implement quicksort algorithm", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Write code for breadth-first search in a graph", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Implement Dijkstra's shortest path algorithm", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Create a linked list with insert and delete methods", "difficulty": "easy"},
    {"category": "Algorithms", "message": "Write code for depth-first search traversal", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Implement a binary search tree with insert/delete", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Create a hash table with collision handling", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Write code to detect cycle in a linked list", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Implement a trie data structure for autocomplete", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Write code for topological sorting", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Implement Kruskal's minimum spanning tree", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Create a min-heap data structure", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Write code to find the middle element of linked list", "difficulty": "easy"},
    {"category": "Algorithms", "message": "Implement dynamic programming for fibonacci", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Write code for matrix multiplication", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Implement a circular buffer", "difficulty": "medium"},
    {"category": "Algorithms", "message": "Create a priority queue using heap", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Write code to check if string is palindrome", "difficulty": "easy"},
    {"category": "Algorithms", "message": "Implement the knapsack problem solution", "difficulty": "hard"},
    {"category": "Algorithms", "message": "Write code for inorder tree traversal without recursion", "difficulty": "medium"},
    
    # Web Development (61-80)
    {"category": "Web", "message": "Create a REST API endpoint for user registration", "difficulty": "medium"},
    {"category": "Web", "message": "Write middleware for JWT authentication", "difficulty": "hard"},
    {"category": "Web", "message": "Implement file upload with progress tracking", "difficulty": "medium"},
    {"category": "Web", "message": "Create a pagination system for API responses", "difficulty": "easy"},
    {"category": "Web", "message": "Write code to handle CORS in a web server", "difficulty": "easy"},
    {"category": "Web", "message": "Implement rate limiting for API endpoints", "difficulty": "hard"},
    {"category": "Web", "message": "Create a WebSocket chat server", "difficulty": "medium"},
    {"category": "Web", "message": "Write code for server-side caching with Redis", "difficulty": "hard"},
    {"category": "Web", "message": "Implement GraphQL schema for a blog", "difficulty": "hard"},
    {"category": "Web", "message": "Create a simple load balancer", "difficulty": "hard"},
    {"category": "Web", "message": "Write code to compress HTTP responses", "difficulty": "medium"},
    {"category": "Web", "message": "Implement session management with cookies", "difficulty": "medium"},
    {"category": "Web", "message": "Create a simple microservices architecture", "difficulty": "hard"},
    {"category": "Web", "message": "Write code for database migration scripts", "difficulty": "medium"},
    {"category": "Web", "message": "Implement input sanitization middleware", "difficulty": "medium"},
    {"category": "Web", "message": "Create an API versioning system", "difficulty": "medium"},
    {"category": "Web", "message": "Write code for health check endpoints", "difficulty": "easy"},
    {"category": "Web", "message": "Implement request logging middleware", "difficulty": "easy"},
    {"category": "Web", "message": "Create a simple API gateway", "difficulty": "hard"},
    {"category": "Web", "message": "Write code for graceful server shutdown", "difficulty": "medium"},
    
    # Database & SQL (81-90)
    {"category": "Database", "message": "Write a SQL query to find duplicate records", "difficulty": "easy"},
    {"category": "Database", "message": "Create an index optimization strategy", "difficulty": "medium"},
    {"category": "Database", "message": "Implement database connection pooling", "difficulty": "hard"},
    {"category": "Database", "message": "Write a complex JOIN query for reporting", "difficulty": "medium"},
    {"category": "Database", "message": "Create a database schema for an e-commerce site", "difficulty": "medium"},
    {"category": "Database", "message": "Implement database transactions with rollback", "difficulty": "hard"},
    {"category": "Database", "message": "Write code for database backup automation", "difficulty": "medium"},
    {"category": "Database", "message": "Create a query to calculate monthly revenue", "difficulty": "medium"},
    {"category": "Database", "message": "Implement full-text search functionality", "difficulty": "hard"},
    {"category": "Database", "message": "Write code to migrate data between schemas", "difficulty": "hard"},
    
    # DevOps & Testing (91-100)
    {"category": "DevOps", "message": "Write a Dockerfile for a Python web application", "difficulty": "medium"},
    {"category": "DevOps", "message": "Create a CI/CD pipeline configuration", "difficulty": "hard"},
    {"category": "DevOps", "message": "Write unit tests for a REST API endpoint", "difficulty": "medium"},
    {"category": "DevOps", "message": "Implement integration tests for database operations", "difficulty": "hard"},
    {"category": "DevOps", "message": "Create a Kubernetes deployment manifest", "difficulty": "hard"},
    {"category": "DevOps", "message": "Write a bash script to monitor disk space", "difficulty": "easy"},
    {"category": "DevOps", "message": "Implement log rotation for application logs", "difficulty": "medium"},
    {"category": "DevOps", "message": "Create a simple monitoring dashboard config", "difficulty": "medium"},
    {"category": "DevOps", "message": "Write code to automate SSL certificate renewal", "difficulty": "hard"},
    {"category": "DevOps", "message": "Create environment-specific configuration files", "difficulty": "easy"},
]


# ============================================================================
# BENCHMARK CLASSES
# ============================================================================

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
    results: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_result(self, time_taken: float, success: bool = True, details: Dict = None):
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
        
        if details:
            self.results.append({**details, "time": time_taken, "success": success})
    
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
            "success_rate": f"{(self.success_count / max(1, self.success_count + self.failure_count)) * 100:.2f}%",
            "detailed_results": self.results[:10]  # First 10 results for reference
        }


class CodingBenchmark:
    """Benchmark LOLANG on coding-related tasks."""
    
    def __init__(self, config: GeminiConfig = None, sample_size: int = 100):
        """
        Initialize coding benchmark.
        
        Args:
            config: Gemini configuration
            sample_size: Number of samples to test (max 100)
        """
        self.config = config or GeminiConfig.get_default_config()
        self.sample_size = min(sample_size, len(CODING_DATASET))
        self.visualizer = MessageVisualizer()
        self.results: List[BenchmarkResult] = []
        self.detailed_results: List[Dict[str, Any]] = []
        
        # Initialize components
        self.agent = AIAgent("Coding-Benchmark-Agent", TerminalColors.CYAN, self.config)
        self.decryptor = LolangDecryptor(self.config)
        
        # Category tracking
        self.categories = {}
    
    def _get_samples_by_category(self) -> Dict[str, List[Dict]]:
        """Group samples by category."""
        categories = {}
        for sample in CODING_DATASET[:self.sample_size]:
            category = sample["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(sample)
        return categories
    
    def _get_samples_by_difficulty(self) -> Dict[str, List[Dict]]:
        """Group samples by difficulty."""
        difficulties = {"easy": [], "medium": [], "hard": []}
        for sample in CODING_DATASET[:self.sample_size]:
            difficulties[sample["difficulty"]].append(sample)
        return difficulties
    
    async def run_coding_benchmark(self) -> BenchmarkResult:
        """Run benchmark on all coding samples."""
        print(TerminalColors.format_header("🚀 LOLANG Coding Benchmark - 100 Samples"))
        print(f"{TerminalColors.BOLD}Model:{TerminalColors.RESET} {self.config.model_name}")
        print(f"{TerminalColors.BOLD}Samples:{TerminalColors.RESET} {self.sample_size}")
        print(f"{TerminalColors.BOLD}Temperature:{TerminalColors.RESET} {self.config.temperature}")
        print(TerminalColors.format_separator('='))
        print()
        
        result = BenchmarkResult(test_name="Coding Dataset Benchmark")
        
        # Process each sample
        for i, sample in enumerate(CODING_DATASET[:self.sample_size], 1):
            start_time = time.time()
            
            try:
                # Display progress
                category_color = TerminalColors.get_role_color(sample["category"])
                print(f"{TerminalColors.BOLD}[{i}/{self.sample_size}]{TerminalColors.RESET} "
                      f"{TerminalColors.colorize(sample['category'], category_color)} "
                      f"({sample['difficulty']}): {sample['message'][:50]}...")
                
                # Test 1: Generate LOLANG response
                message_history = [
                    {"role": "user", "content": sample["message"]},
                    {"role": "system", "content": "Respond using LOLANG language for AI-to-AI communication"}
                ]
                
                response_start = time.time()
                response = self.agent.chat(message_history)
                response_time = time.time() - response_start
                
                if not response or response.startswith("[Error"):
                    raise Exception(f"AI response failed: {response}")
                
                # Test 2: Decrypt the response
                decrypt_start = time.time()
                decrypted = self.decryptor.decrypt_sync(response)
                decrypt_time = time.time() - decrypt_start
                
                if not decrypted or decrypted.startswith("[Decryption failed"):
                    raise Exception(f"Decryption failed: {decrypted}")
                
                elapsed = time.time() - start_time
                
                # Record result
                result.add_result(elapsed, success=True, details={
                    "index": i,
                    "category": sample["category"],
                    "difficulty": sample["difficulty"],
                    "message": sample["message"],
                    "response_time": round(response_time, 3),
                    "decrypt_time": round(decrypt_time, 3),
                    "response_preview": response[:100] + "..." if len(response) > 100 else response,
                })
                
                # Update category stats
                if sample["category"] not in self.categories:
                    self.categories[sample["category"]] = []
                self.categories[sample["category"]].append(elapsed)
                
                # Store detailed result
                self.detailed_results.append({
                    "index": i,
                    "category": sample["category"],
                    "difficulty": sample["difficulty"],
                    "original_message": sample["message"],
                    "lolang_response": response,
                    "decrypted_message": decrypted,
                    "total_time": round(elapsed, 3),
                    "response_time": round(response_time, 3),
                    "decrypt_time": round(decrypt_time, 3),
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                
                print(f"  ✓ Total: {elapsed:.3f}s (Response: {response_time:.3f}s, Decrypt: {decrypt_time:.3f}s)")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                elapsed = time.time() - start_time
                result.add_result(elapsed, success=False, details={
                    "index": i,
                    "category": sample["category"],
                    "difficulty": sample["difficulty"],
                    "message": sample["message"],
                    "error": str(e)
                })
                
                print(f"  ✗ Failed: {str(e)[:80]}")
                logger.error(f"Sample {i} failed: {e}")
        
        return result
    
    async def run_category_benchmarks(self) -> List[BenchmarkResult]:
        """Run benchmarks grouped by category."""
        print(TerminalColors.format_header("📊 Category-wise Benchmark"))
        
        categories = self._get_samples_by_category()
        results = []
        
        for category, samples in categories.items():
            print(f"\n{TerminalColors.BOLD}{category} ({len(samples)} samples){TerminalColors.RESET}")
            
            result = BenchmarkResult(test_name=f"Category: {category}")
            
            for i, sample in enumerate(samples, 1):
                start_time = time.time()
                
                try:
                    message_history = [
                        {"role": "user", "content": sample["message"]}
                    ]
                    
                    response = self.agent.chat(message_history)
                    
                    if not response or response.startswith("[Error"):
                        raise Exception(response)
                    
                    elapsed = time.time() - start_time
                    result.add_result(elapsed, success=True, details={
                        "message": sample["message"],
                        "difficulty": sample["difficulty"]
                    })
                    
                    print(f"  ✓ [{i}/{len(samples)}] {sample['message'][:40]}... - {elapsed:.3f}s")
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    elapsed = time.time() - start_time
                    result.add_result(elapsed, success=False, details={
                        "message": sample["message"],
                        "error": str(e)
                    })
                    print(f"  ✗ [{i}/{len(samples)}] Failed: {str(e)[:50]}")
            
            results.append(result)
            print(f"  {TerminalColors.colorize(f'Success: {result.success_count}/{result.total_requests} '
                                               f'({result.success_rate})', TerminalColors.GREEN)}")
        
        self.results.extend(results)
        return results
    
    async def run_difficulty_benchmarks(self) -> List[BenchmarkResult]:
        """Run benchmarks grouped by difficulty."""
        print(TerminalColors.format_header("🎯 Difficulty-wise Benchmark"))
        
        difficulties = self._get_samples_by_difficulty()
        results = []
        
        for difficulty, samples in difficulties.items():
            if not samples:
                continue
                
            print(f"\n{TerminalColors.BOLD}{difficulty.upper()} ({len(samples)} samples){TerminalColors.RESET}")
            
            result = BenchmarkResult(test_name=f"Difficulty: {difficulty}")
            
            for i, sample in enumerate(samples, 1):
                start_time = time.time()
                
                try:
                    message_history = [{"role": "user", "content": sample["message"]}]
                    response = self.agent.chat(message_history)
                    
                    if not response or response.startswith("[Error"):
                        raise Exception(response)
                    
                    elapsed = time.time() - start_time
                    result.add_result(elapsed, success=True, details={
                        "message": sample["message"],
                        "category": sample["category"]
                    })
                    
                    print(f"  ✓ [{i}/{len(samples)}] {elapsed:.3f}s")
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    elapsed = time.time() - start_time
                    result.add_result(elapsed, success=False, details={
                        "message": sample["message"],
                        "error": str(e)
                    })
                    print(f"  ✗ [{i}/{len(samples)}] Failed: {str(e)[:50]}")
            
            results.append(result)
            print(f"  {TerminalColors.colorize(f'Success: {result.success_count}/{result.total_requests} '
                                               f'({result.success_rate})', TerminalColors.GREEN)}")
        
        self.results.extend(results)
        return results
    
    def _print_detailed_summary(self, main_result: BenchmarkResult):
        """Print comprehensive summary report."""
        print("\n")
        print(TerminalColors.format_header("📈 Comprehensive Benchmark Summary"))
        print()
        
        # Overall Statistics
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  OVERALL STATISTICS{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"  Total Samples: {TerminalColors.BOLD}{main_result.total_requests}{TerminalColors.RESET}")
        print(f"  Successful: {TerminalColors.colorize(str(main_result.success_count), TerminalColors.GREEN)}")
        print(f"  Failed: {TerminalColors.colorize(str(main_result.failure_count), TerminalColors.RED if main_result.failure_count > 0 else TerminalColors.GREEN)}")
        print(f"  Success Rate: {TerminalColors.BOLD}{main_result.success_rate}{TerminalColors.RESET}")
        print(f"  Total Time: {TerminalColors.BOLD}{main_result.total_time:.3f}s{TerminalColors.RESET}")
        print(f"  Average Time: {TerminalColors.BOLD}{main_result.avg_time:.3f}s{TerminalColors.RESET}")
        print(f"  Min Time: {main_result.min_time:.3f}s")
        print(f"  Max Time: {main_result.max_time:.3f}s")
        print(f"  Std Deviation: {statistics.stdev(main_result.times) if len(main_result.times) > 1 else 0:.3f}s")
        print()
        
        # Category Breakdown
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  CATEGORY BREAKDOWN{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        
        for category, times in self.categories.items():
            avg_time = statistics.mean(times)
            count = len(times)
            print(f"  {category:15} | {count:3} samples | Avg: {avg_time:.3f}s | "
                  f"Min: {min(times):.3f}s | Max: {max(times):.3f}s")
        print()
        
        # Difficulty Breakdown
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  DIFFICULTY BREAKDOWN{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        
        difficulties = {"easy": [], "medium": [], "hard": []}
        for sample_result in self.detailed_results:
            if sample_result.get("success"):
                difficulties[sample_result["difficulty"]].append(sample_result["total_time"])
        
        for difficulty, times in difficulties.items():
            if times:
                avg_time = statistics.mean(times)
                print(f"  {difficulty.upper():10} | {len(times):3} samples | Avg: {avg_time:.3f}s | "
                      f"Min: {min(times):.3f}s | Max: {max(times):.3f}s")
        print()
        
        # Performance Distribution
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  PERFORMANCE DISTRIBUTION{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        
        if main_result.times:
            sorted_times = sorted(main_result.times)
            percentiles = [10, 25, 50, 75, 90, 95, 99]
            
            for p in percentiles:
                idx = int(len(sorted_times) * p / 100) - 1
                if idx >= 0:
                    print(f"  P{p:2}: {sorted_times[idx]:.3f}s")
        print()
        
        # Top 5 Fastest
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  TOP 5 FASTEST{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        
        sorted_results = sorted(self.detailed_results, key=lambda x: x.get("total_time", float('inf')))
        for i, res in enumerate(sorted_results[:5], 1):
            print(f"  {i}. [{res['category']}] {res['original_message'][:50]} - "
                  f"{res['total_time']:.3f}s")
        print()
        
        # Top 5 Slowest
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}  TOP 5 SLOWEST{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'='*80}{TerminalColors.RESET}")
        
        sorted_results_desc = sorted(self.detailed_results, key=lambda x: x.get("total_time", 0), reverse=True)
        for i, res in enumerate(sorted_results_desc[:5], 1):
            print(f"  {i}. [{res['category']}] {res['original_message'][:50]} - "
                  f"{res['total_time']:.3f}s")
        print()
        
        print(TerminalColors.format_separator('='))
    
    def save_detailed_results(self, filename: str = "coding_benchmark_results.json"):
        """
        Save comprehensive benchmark results to JSON.
        
        Args:
            filename: Output filename
        """
        # Aggregate statistics
        category_stats = {}
        for category, times in self.categories.items():
            category_stats[category] = {
                "count": len(times),
                "avg_time": round(statistics.mean(times), 3),
                "min_time": round(min(times), 3),
                "max_time": round(max(times), 3),
                "std_dev": round(statistics.stdev(times), 3) if len(times) > 1 else 0
            }
        
        # Difficulty statistics
        difficulty_stats = {}
        difficulties = {"easy": [], "medium": [], "hard": []}
        for sample_result in self.detailed_results:
            if sample_result.get("success"):
                difficulties[sample_result["difficulty"]].append(sample_result["total_time"])
        
        for difficulty, times in difficulties.items():
            if times:
                difficulty_stats[difficulty] = {
                    "count": len(times),
                    "avg_time": round(statistics.mean(times), 3),
                    "min_time": round(min(times), 3),
                    "max_time": round(max(times), 3)
                }
        
        results_data = {
            "benchmark_metadata": {
                "benchmark_date": datetime.now().isoformat(),
                "model": self.config.model_name,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "total_samples": self.sample_size,
                "successful_samples": len([r for r in self.detailed_results if r.get("success")]),
                "failed_samples": len([r for r in self.detailed_results if not r.get("success")])
            },
            "overall_statistics": {
                "total_time": round(sum(r.get("total_time", 0) for r in self.detailed_results), 3),
                "avg_time_per_sample": round(statistics.mean([r["total_time"] for r in self.detailed_results if r.get("success")]), 3),
                "min_time": round(min([r["total_time"] for r in self.detailed_results if r.get("success")]), 3),
                "max_time": round(max([r["total_time"] for r in self.detailed_results if r.get("success")]), 3),
            },
            "category_statistics": category_stats,
            "difficulty_statistics": difficulty_stats,
            "detailed_results": self.detailed_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{TerminalColors.colorize('✓', TerminalColors.GREEN)} Results saved to {TerminalColors.BOLD}{filename}{TerminalColors.RESET}")
        print(f"  File size: {os.path.getsize(filename) / 1024:.2f} KB")


async def main():
    """Main entry point."""
    logging.basicConfig(level=logging.WARNING)
    
    # Validate configuration
    config = GeminiConfig.get_default_config()
    
    if not config.validate():
        print(TerminalColors.colorize(
            "❌ ERROR: Invalid configuration. Please set GEMINI_API_KEY in .env file.",
            TerminalColors.RED
        ))
        print(TerminalColors.colorize(
            "   Copy .env.example to .env and add your API key.",
            TerminalColors.YELLOW
        ))
        return
    
    # Ask user for sample size
    print(TerminalColors.format_header("⚙️  Benchmark Configuration"))
    sample_size = 100  # Default to full dataset
    
    print(f"{TerminalColors.BOLD}Dataset Size:{TerminalColors.RESET} 100 coding samples")
    print(f"{TerminalColors.BOLD}Categories:{TerminalColors.RESET} Python, JavaScript, Algorithms, Web, Database, DevOps")
    print(f"{TerminalColors.BOLD}Difficulties:{TerminalColors.RESET} Easy, Medium, Hard")
    print()
    
    # Create benchmark
    benchmark = CodingBenchmark(config=config, sample_size=sample_size)
    
    try:
        # Run main coding benchmark
        main_result = await benchmark.run_coding_benchmark()
        
        # Run category-wise benchmarks
        await benchmark.run_category_benchmarks()
        
        # Run difficulty-wise benchmarks
        await benchmark.run_difficulty_benchmarks()
        
        # Print comprehensive summary
        benchmark._print_detailed_summary(main_result)
        
        # Save detailed results
        benchmark.save_detailed_results()
        
        # Print category and additional results
        if benchmark.results:
            print("\n")
            print(TerminalColors.format_header("📚 Additional Benchmark Results"))
            for result in benchmark.results:
                data = result.to_dict()
                print(f"\n{TerminalColors.BOLD}{data['test_name']}{TerminalColors.RESET}")
                print(f"  Success: {data['success_count']}/{data['total_requests']} ({data['success_rate']})")
                print(f"  Avg Time: {data['avg_time']:.3f}s")
                print(f"  Total Time: {data['total_time']:.3f}s")
        
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\n\n⚠️  Benchmark interrupted", TerminalColors.YELLOW))
        if benchmark.detailed_results:
            print(TerminalColors.colorize(f"   Partial results: {len(benchmark.detailed_results)} samples processed", 
                                         TerminalColors.YELLOW))
            benchmark.save_detailed_results("coding_benchmark_partial.json")
    except Exception as e:
        print(TerminalColors.colorize(f"\n\n❌ Benchmark error: {e}", TerminalColors.RED))
        logger.error(f"Benchmark error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\n⚠️  Benchmark interrupted", TerminalColors.YELLOW))
