#!/usr/bin/env python3
"""
Initialize SQLite database with the required tables
"""

import sqlite3
import os
from pathlib import Path

def create_database():
    """Create SQLite database with all required tables"""
    
    # Database file path
    db_path = Path('./test.db')
    
    # Remove existing database if it exists
    if db_path.exists():
        os.remove(db_path)
        print("🗑️  Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🏗️  Creating tables...")
    
    # User accounts table
    cursor.execute("""
        CREATE TABLE user_accounts (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            profile_completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created user_accounts table")
    
    # Refresh tokens table
    cursor.execute("""
        CREATE TABLE refresh_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT NOT NULL,
            expires_at DATETIME NOT NULL,
            revoked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE
        )
    """)
    print("✓ Created refresh_tokens table")
    
    # User profiles table
    cursor.execute("""
        CREATE TABLE user_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            age INTEGER,
            income REAL,
            savings REAL,
            expenses REAL,
            financial_goals TEXT,
            risk_tolerance TEXT DEFAULT 'medium',
            investment_experience TEXT DEFAULT 'beginner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE
        )
    """)
    print("✓ Created user_profiles table")
    
    # Financial goals table
    cursor.execute("""
        CREATE TABLE financial_goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL DEFAULT 0,
            target_date DATE,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE
        )
    """)
    print("✓ Created financial_goals table")
    
    # Budget categories table
    cursor.execute("""
        CREATE TABLE budget_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            budgeted_amount REAL NOT NULL,
            spent_amount REAL DEFAULT 0,
            category_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE,
            UNIQUE(user_id, category_name)
        )
    """)
    print("✓ Created budget_categories table")
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER,
            amount REAL NOT NULL,
            description TEXT,
            transaction_type TEXT NOT NULL,
            transaction_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES budget_categories(category_id) ON DELETE SET NULL
        )
    """)
    print("✓ Created transactions table")
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX idx_user_id ON refresh_tokens(user_id)")
    cursor.execute("CREATE INDEX idx_expires_at ON refresh_tokens(expires_at)")
    cursor.execute("CREATE INDEX idx_user_date ON transactions(user_id, transaction_date)")
    cursor.execute("CREATE INDEX idx_category ON transactions(category_id)")
    print("✓ Created indexes")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized successfully: {db_path.absolute()}")
    print("📊 Tables created:")
    print("   - user_accounts")
    print("   - refresh_tokens")  
    print("   - user_profiles")
    print("   - financial_goals")
    print("   - budget_categories")
    print("   - transactions")

if __name__ == "__main__":
    create_database()