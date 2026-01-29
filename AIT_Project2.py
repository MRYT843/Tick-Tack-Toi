import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# ==================== OOP Classes ====================

class Student:
    """Class to represent a student and their attendance"""
    
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.total_classes = 0
        self.present_count = 0
        self.attendance_history = []
    
    def mark_present(self):
        """Mark student as present"""
        self.total_classes += 1
        self.present_count += 1
        self.attendance_history.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'status': 'Present'
        })
    
    def mark_absent(self):
        """Mark student as absent"""
        self.total_classes += 1
        self.attendance_history.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'status': 'Absent'
        })
    
    def attendance_percentage(self):
        """Calculate and return attendance percentage"""
        if self.total_classes == 0:
            return 0
        return (self.present_count / self.total_classes) * 100
    
    def to_dict(self):
        """Convert student to dictionary for JSON storage"""
        return {
            'name': self.name,
            'roll_number': self.roll_number,
            'total_classes': self.total_classes,
            'present_count': self.present_count,
            'attendance_history': self.attendance_history
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create student from dictionary"""
        student = cls(data['name'], data['roll_number'])
        student.total_classes = data['total_classes']
        student.present_count = data['present_count']
        student.attendance_history = data.get('attendance_history', [])
        return student


class AttendanceManager:
    """Class to manage all students and their attendance"""
    
    # List of 20 realistic names for students
    STUDENT_NAMES = [
        "Ali", "Ahmed", "Ayesha", "Fatima", "Hassan", 
        "Hussain", "Zain", "Sana", "Omar", "Noor",
        "Maha", "Hana", "Karim", "Layla", "Sara",
        "Tariq", "Amira", "Jamal", "Leila", "Rashid"
    ]
    
    def __init__(self):
        self.students_list = {}
        self._preload_students()
    
    def _preload_students(self):
        """Preload 20 students with realistic names and roll numbers 1-20"""
        for i in range(1, 21):
            name = self.STUDENT_NAMES[i - 1]
            roll_number = i
            self.students_list[roll_number] = Student(name, roll_number)
    
    def add_student(self, name, roll_number):
        """Add a new student"""
        if roll_number in self.students_list:
            return False, f"Roll number {roll_number} already exists!"
        
        self.students_list[roll_number] = Student(name, roll_number)
        return True, f"Student {name} (Roll: {roll_number}) added successfully!"
    
    def get_student(self, roll_number):
        """Get a student by roll number"""
        return self.students_list.get(roll_number)
    
    def mark_attendance(self, roll_number, status):
        """Mark attendance for a student"""
        student = self.get_student(roll_number)
        if not student:
            return False, f"Student with roll number {roll_number} not found!"
        
        if status.lower() == 'present':
            student.mark_present()
            return True, f"Marked {student.name} as Present!"
        elif status.lower() == 'absent':
            student.mark_absent()
            return True, f"Marked {student.name} as Absent!"
        else:
            return False, "Invalid status. Use 'present' or 'absent'."
    
    def get_all_records(self):
        """Get all attendance records"""
        records = []
        for roll_number, student in sorted(self.students_list.items()):
            records.append({
                'Roll Number': roll_number,
                'Name': student.name,
                'Total Classes': student.total_classes,
                'Present': student.present_count,
                'Absent': student.total_classes - student.present_count,
                'Attendance %': f"{student.attendance_percentage():.2f}%"
            })
        return records
    
    def get_student_record(self, roll_number):
        """Get attendance record of a specific student"""
        student = self.get_student(roll_number)
        if not student:
            return None
        
        return {
            'Name': student.name,
            'Roll Number': roll_number,
            'Total Classes': student.total_classes,
            'Present': student.present_count,
            'Absent': student.total_classes - student.present_count,
            'Attendance %': f"{student.attendance_percentage():.2f}%",
            'History': student.attendance_history
        }
    
    def save_to_json(self, filename='attendance_data.json'):
        """Save all data to JSON file"""
        data = {
            roll_num: student.to_dict()
            for roll_num, student in self.students_list.items()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_from_json(self, filename='attendance_data.json'):
        """Load data from JSON file - updates existing students' attendance only"""
        if not Path(filename).exists():
            return
        
        with open(filename, 'r') as f:
            data = json.load(f)
            for roll_num, student_data in data.items():
                roll_num_int = int(roll_num)
                # Only update if student exists (don't add new ones)
                if roll_num_int in self.students_list:
                    student = self.students_list[roll_num_int]
                    student.total_classes = student_data.get('total_classes', 0)
                    student.present_count = student_data.get('present_count', 0)
                    student.attendance_history = student_data.get('attendance_history', [])


class ChatBot:
    """Rule-based chatbot for attendance management"""
    
    def __init__(self, manager):
        self.manager = manager
        self.commands = {
            'add': self.cmd_add_student,
            'mark': self.cmd_mark_attendance,
            'show': self.cmd_show_all_attendance,
            'attendance': self.cmd_show_student_attendance,
            'list': self.cmd_list_students,
            'help': self.cmd_help,
            'delete': self.cmd_delete_student,
            'p': self.cmd_mark_present_shortcut,
            'a': self.cmd_mark_absent_shortcut,
        }
    
    def process_message(self, message):
        """Process user message and return response"""
        message = message.strip().lower()
        
        if not message:
            return "Please enter a command. Type 'help' for available commands."
        
        tokens = message.split()
        command = tokens[0]
        
        if command in self.commands:
            return self.commands[command](tokens)
        else:
            return f"Unknown command: '{command}'. Type 'help' for available commands."
    
    def cmd_mark_present_shortcut(self, tokens):
        """Handle: p <roll_number> or p all - Shortcut for marking present"""
        if len(tokens) < 2:
            return "Usage: p <roll_number> or p all"
        
        # Check if marking all students
        if tokens[1].lower() == 'all':
            return self.cmd_mark_all_present()
        
        try:
            roll_number = int(tokens[1])
        except ValueError:
            return "Roll number must be a number!"
        
        success, message = self.manager.mark_attendance(roll_number, 'present')
        return message
    
    def cmd_mark_all_present(self):
        """Mark all students as present"""
        count = 0
        for roll_number in self.manager.students_list.keys():
            self.manager.mark_attendance(roll_number, 'present')
            count += 1
        return f"✅ Marked all {count} students as present!"
    
    def cmd_mark_absent_shortcut(self, tokens):
        """Handle: a <roll_number> - Shortcut for marking absent"""
        if len(tokens) < 2:
            return "Usage: a <roll_number>"
        
        try:
            roll_number = int(tokens[1])
        except ValueError:
            return "Roll number must be a number!"
        
        success, message = self.manager.mark_attendance(roll_number, 'absent')
        return message
    
    def cmd_add_student(self, tokens):
        """Handle: add student <name> <roll_number>"""
        if len(tokens) < 4:
            return "Usage: add student <name> <roll_number>"
        
        name = tokens[2]
        try:
            roll_number = int(tokens[3])
        except ValueError:
            return "Roll number must be a number!"
        
        success, message = self.manager.add_student(name, roll_number)
        return message
    
    def cmd_mark_attendance(self, tokens):
        """Handle: mark <present|absent> <roll_number>"""
        if len(tokens) < 3:
            return "Usage: mark <present|absent> <roll_number>"
        
        status = tokens[1]
        try:
            roll_number = int(tokens[2])
        except ValueError:
            return "Roll number must be a number!"
        
        success, message = self.manager.mark_attendance(roll_number, status)
        return message
    
    def cmd_show_all_attendance(self, tokens):
        """Handle: show attendance"""
        records = self.manager.get_all_records()
        if not records:
            return "No students in the system yet."
        return ('show_table', records)
    
    def cmd_show_student_attendance(self, tokens):
        """Handle: attendance of <roll_number>"""
        if len(tokens) < 3:
            return "Usage: attendance of <roll_number>"
        
        try:
            roll_number = int(tokens[2])
        except ValueError:
            return "Roll number must be a number!"
        
        record = self.manager.get_student_record(roll_number)
        if not record:
            return f"No student found with roll number {roll_number}"
        return ('show_detail', record)
    
    def cmd_list_students(self, tokens):
        """Handle: list"""
        if not self.manager.students_list:
            return "No students in the system yet."
        
        students = []
        for roll_num in sorted(self.manager.students_list.keys()):
            student = self.manager.students_list[roll_num]
            students.append({
                'Roll Number': roll_num,
                'Name': student.name
            })
        return ('show_list', students)
    
    def cmd_delete_student(self, tokens):
        """Handle: delete <roll_number>"""
        if len(tokens) < 2:
            return "Usage: delete <roll_number>"
        
        try:
            roll_number = int(tokens[1])
        except ValueError:
            return "Roll number must be a number!"
        
        if roll_number not in self.manager.students_list:
            return f"Student with roll number {roll_number} not found!"
        
        student_name = self.manager.students_list[roll_number].name
        del self.manager.students_list[roll_number]
        return f"Student {student_name} deleted successfully!"
    
    def cmd_help(self, tokens):
        """Handle: help"""
        help_text = """
🤖 **AttendBot - Available Commands:**

**System Info:**
  `help` - Show this message

**Add Student (beyond 200):**
  `add student <name> <roll_number>`
  Example: `add student Ali 201`

**Mark Attendance (Full):**
  `mark present <roll_number>` - Mark student as present
  `mark absent <roll_number>` - Mark student as absent
  Example: `mark present 12`

**Mark Attendance (Shortcuts) ⚡:**
  `p <roll_number>` - Quick mark as present
  `p all` - Mark ALL students as present
  `a <roll_number>` - Quick mark as absent
  Example: `p 12` or `p all` or `a 5`

**View Attendance:**
  `show attendance` - Show all students attendance
  `attendance of <roll_number>` - Show specific student
  Example: `attendance of 12`

**List Students:**
  `list` - Show all enrolled students

**Delete Student:**
  `delete <roll_number>`
  Example: `delete 12`

**System Status:**
  Total Students: 20 (preloaded with realistic names)
  Roll Numbers: 1-20
        """
        return help_text


# ==================== Streamlit UI ====================

def initialize_session():
    """Initialize session state"""
    if 'manager' not in st.session_state:
        st.session_state.manager = AttendanceManager()
        st.session_state.manager.load_from_json()
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatBot(st.session_state.manager)
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm AttendBot with 20 preloaded students. Type 'help' to see available commands."}
        ]


def save_data():
    """Save attendance data to JSON"""
    st.session_state.manager.save_to_json()


def main():
    st.set_page_config(page_title="AttendBot", layout="wide")
    
    initialize_session()
    
    # Header
    st.title("📚 AttendBot - Attendance Management System")
    st.markdown("*20 Preloaded Students | Rule-based Chatbot Interface*")
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
        
        # Input
        user_input = st.chat_input("Enter command...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Process message
            response = st.session_state.chatbot.process_message(user_input)
            
            # Handle different response types
            if isinstance(response, tuple):
                response_type, data = response
                
                if response_type == 'show_table':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Here's the attendance data:",
                        "data": data,
                        "type": "table"
                    })
                elif response_type == 'show_detail':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Attendance record for {data['Name']}:",
                        "data": data,
                        "type": "detail"
                    })
                elif response_type == 'show_list':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Enrolled students:",
                        "data": data,
                        "type": "list"
                    })
            else:
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            save_data()
            st.rerun()
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        total_students = len(st.session_state.manager.students_list)
        st.metric("Total Students", total_students)
        
        if total_students > 0:
            # Get students with attendance history
            students_with_attendance = [s for s in st.session_state.manager.students_list.values() if s.total_classes > 0]
            
            if students_with_attendance:
                # Find the max classes held (latest session)
                max_classes = max(s.total_classes for s in students_with_attendance)
                
                # Count students present in current session (last marked)
                present_in_current = sum(1 for s in students_with_attendance 
                                        if s.attendance_history and s.attendance_history[-1]['status'] == 'Present')
                absent_in_current = sum(1 for s in students_with_attendance 
                                       if s.attendance_history and s.attendance_history[-1]['status'] == 'Absent')
                
                st.metric("Class Sessions Held", max_classes)
                st.metric("Present (Latest)", present_in_current)
                st.metric("Absent (Latest)", absent_in_current)
                
                # Overall attendance
                total_present = sum(s.present_count for s in students_with_attendance)
                total_records = sum(s.total_classes for s in students_with_attendance)
                overall_attendance = (total_present / total_records * 100) if total_records > 0 else 0
                st.metric("Overall Attendance %", f"{overall_attendance:.2f}%")
            else:
                st.info("No attendance records yet. Start marking attendance!")
    
    # Display data in messages
    st.markdown("---")
    
    if st.session_state.messages:
        # Display all messages including data
        for i, message in enumerate(st.session_state.messages):
            if message.get("type") == "table":
                st.write("📊 **Attendance Records:**")
                st.dataframe(message["data"], use_container_width=True, height=400)
            elif message.get("type") == "detail":
                data = message["data"]
                st.write(f"📋 **Student: {data['Name']} (Roll: {data['Roll Number']})**")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Classes", data['Total Classes'])
                col2.metric("Present", data['Present'])
                col3.metric("Absent", data['Absent'])
                col4.metric("Attendance", data['Attendance %'])
                
                if data['History']:
                    st.write("**Attendance History:**")
                    st.dataframe(data['History'], use_container_width=True)
            
            elif message.get("type") == "list":
                st.write("👥 **Student List:**")
                st.dataframe(message["data"], use_container_width=True, height=400)


if __name__ == "__main__":
    main()
