#!/usr/bin/env python3
"""
Test script to check database connection and operations
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.connection import get_connection
from db.init_db import init_db

def test_database():
    print("=== Database Connection Test ===")
    
    try:
        # Test 1: Initialize database
        print("1. Initializing database...")
        init_db()
        print("   ✓ Database initialized successfully")
        
        # Test 2: Test connection
        print("2. Testing database connection...")
        conn = get_connection()
        print("   ✓ Connection established")
        
        # Test 3: Create a test task
        print("3. Testing task creation...")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, deadline, completed) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, ("Test Task", "This is a test task", "High", "2024-12-25 10:00:00", False))
        
        task_id = cursor.fetchone()[0]
        conn.commit()
        print(f"   ✓ Test task created with ID: {task_id}")
        
        # Test 4: Retrieve tasks
        print("4. Testing task retrieval...")
        cursor.execute("SELECT id, title, description, priority, deadline, completed FROM tasks")
        tasks = cursor.fetchall()
        print(f"   ✓ Found {len(tasks)} task(s)")
        
        for task in tasks:
            print(f"      - ID: {task[0]}, Title: {task[1]}, Priority: {task[3]}")
        
        # Test 5: Update task
        print("5. Testing task update...")
        cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (True, task_id))
        conn.commit()
        print("   ✓ Task updated successfully")
        
        # Test 6: Delete test task
        print("6. Cleaning up test task...")
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        print("   ✓ Test task deleted")
        
        conn.close()
        print("\n=== All tests PASSED! Database is working correctly ===")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test FAILED: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
