from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset database sequences to prevent ID conflicts after loading fixtures'

    def handle(self, *args, **options):
        """
        Reset all sequences to the maximum ID + 1 for each table.
        This prevents new records from getting IDs that already exist in fixture data.
        """
        with connection.cursor() as cursor:
            # Get database vendor (postgresql, sqlite, mysql, etc.)
            vendor = connection.vendor
            
            if vendor == 'postgresql':
                # PostgreSQL: Reset sequences for all tables
                cursor.execute("""
                    SELECT 
                        table_name, 
                        column_name
                    FROM information_schema.columns
                    WHERE column_default LIKE 'nextval%'
                    AND table_schema = 'public';
                """)
                
                sequences = cursor.fetchall()
                for table_name, column_name in sequences:
                    sequence_name = f"{table_name}_{column_name}_seq"
                    cursor.execute(f"""
                        SELECT setval(
                            '{sequence_name}',
                            COALESCE((SELECT MAX({column_name}) FROM {table_name}), 1),
                            true
                        );
                    """)
                    self.stdout.write(
                        self.style.SUCCESS(f'Reset sequence for {table_name}.{column_name}')
                    )
                    
            elif vendor == 'sqlite':
                # SQLite: Reset sequences in sqlite_sequence table
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name != 'sqlite_sequence';
                """)
                
                tables = cursor.fetchall()
                for (table_name,) in tables:
                    # Get max ID for this table
                    try:
                        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
                        max_id = cursor.fetchone()[0]
                        
                        if max_id is not None:
                            # Update or insert into sqlite_sequence
                            cursor.execute(f"""
                                INSERT OR REPLACE INTO sqlite_sequence (name, seq) 
                                VALUES ('{table_name}', {max_id})
                            """)
                            self.stdout.write(
                                self.style.SUCCESS(f'Reset sequence for {table_name} to {max_id}')
                            )
                    except Exception as e:
                        # Table might not have an id column, skip it
                        continue
                        
            elif vendor == 'mysql':
                # MySQL: Reset auto_increment values
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                for (table_name,) in tables:
                    cursor.execute(f"SELECT MAX(id) FROM {table_name}")
                    max_id = cursor.fetchone()[0]
                    
                    if max_id is not None:
                        cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = {max_id + 1}")
                        self.stdout.write(
                            self.style.SUCCESS(f'Reset auto_increment for {table_name} to {max_id + 1}')
                        )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Unsupported database vendor: {vendor}')
                )
                return

        self.stdout.write(
            self.style.SUCCESS('\n✅ All sequences have been reset successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS('New records will now use IDs that don\'t conflict with fixture data.')
        )
