from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models import db, Project, LineItem, BidHistory, RateCard
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "bid_assist.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with app
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def serve_index():
        """Serve the main index.html file"""
        return send_from_directory('static', 'index.html')
    
    @app.route('/api/projects', methods=['GET'])
    def get_projects():
        """Get all projects"""
        try:
            projects = Project.query.all()
            return jsonify({
                'success': True,
                'data': [project.to_dict() for project in projects]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/projects', methods=['POST'])
    def create_project():
        """Create a new project"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data or 'name' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Project name is required'
                }), 400
            
            # Create new project
            project = Project(
                name=data['name'],
                description=data.get('description', '')
            )
            
            db.session.add(project)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': project.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/projects/<int:project_id>', methods=['GET'])
    def get_project(project_id):
        """Get a specific project"""
        try:
            project = Project.query.get_or_404(project_id)
            return jsonify({
                'success': True,
                'data': project.to_dict()
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/projects/<int:project_id>', methods=['PUT'])
    def update_project(project_id):
        """Update a project"""
        try:
            project = Project.query.get_or_404(project_id)
            data = request.get_json()
            
            if 'name' in data:
                project.name = data['name']
            if 'description' in data:
                project.description = data['description']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': project.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/projects/<int:project_id>', methods=['DELETE'])
    def delete_project(project_id):
        """Delete a project"""
        try:
            project = Project.query.get_or_404(project_id)
            db.session.delete(project)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Project deleted successfully'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'success': True,
            'message': 'BidAssist API is running'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)