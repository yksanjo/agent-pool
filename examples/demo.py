#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import AgentPool
def main():
    print("Agent Pool Demo")
    p = AgentPool()
    p.add_agent("a1", 10)
    p.add_agent("a2", 5)
    a = p.acquire()
    print(f"Acquired: {a}")
    p.release(a)
    print("Done!")
if __name__ == "__main__": main()
