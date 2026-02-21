# utils/ai_helper.py
import os
import random
from datetime import datetime, timedelta
import openai
import json
from flask import current_app
import logging

logger = logging.getLogger(__name__)



class AIHelper:
    def __init__(self):
        self.enabled = True

    def analyze_task(self, description):
        """Analyze task using OpenAI and return AI insights"""
        if not self.enabled or not description:
            return self._get_default_insights()

        try:
            api_key = current_app.config.get('OPENAI_API_KEY')
            if not api_key:
                return self._get_default_insights()

            openai.api_key = api_key
            
            prompt = f"""Analyze the following task and provide insights in JSON format:
Task: {description}

Provide response as JSON with these fields (use numbers where applicable):
- estimated_hours: estimated hours to complete (float 0.5-100)
- complexity_score: 1-5 scale
- recommended_approach: brief approach string
- potential_blockers: list of 2-3 potential issues
- suggested_resources: list of 2-3 helpful resources
- confidence_score: 0.5-0.95 confidence in estimate

Return ONLY valid JSON, no other text."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            insights = json.loads(content)
            
            # Ensure all required fields exist and have correct types
            return {
                'estimated_completion_time': float(insights.get('estimated_hours', 4.0)),
                'complexity_score': int(insights.get('complexity_score', 3)),
                'recommended_approach': str(insights.get('recommended_approach', 'Standard approach')),
                'potential_blockers': list(insights.get('potential_blockers', [])),
                'suggested_resources': list(insights.get('suggested_resources', [])),
                'confidence_score': float(insights.get('confidence_score', 0.7)),
                'similar_tasks_completed': random.randint(0, 5)
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error from OpenAI: {e}")
            return self._get_default_insights()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_default_insights()

    def _get_default_insights(self):
        """Return default insights when AI is disabled"""
        return {
            'estimated_completion_time': 4.0,
            'suggested_resources': [],
            'complexity_score': 3,
            'recommended_approach': 'Standard approach',
            'confidence_score': 0.5,
            'potential_blockers': [],
            'similar_tasks_completed': 0
        }

    def prioritize_tasks(self, tasks):
        """AI-based task prioritization using OpenAI"""
        if not tasks:
            return []
        
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            # Fallback to default prioritization
            return sorted(tasks, key=lambda x: (
                -x.get('priority', 3),
                -x.get('impact', 5),
                x.get('due_date', datetime.max)
            ))
        
        try:
            openai.api_key = api_key
            
            task_list = "\n".join([
                f"- {t.get('title', 'Untitled')} (Priority: {t.get('priority', 3)}, Impact: {t.get('impact', 5)}, Due: {t.get('due_date', 'N/A')})"
                for t in tasks[:10]  # Limit to 10 tasks for API call
            ])
            
            prompt = f"""Given these tasks, return a JSON array of task indices in prioritized order (most important first):
{task_list}

Respond with ONLY a JSON array like: [0, 2, 1, 3] - no other text."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=100
            )
            
            content = response.choices[0].message.content.strip()
            priority_indices = json.loads(content)
            
            # Reorder tasks based on AI recommendation
            prioritized = [tasks[i] for i in priority_indices if i < len(tasks)]
            # Add any remaining tasks not returned by AI
            remaining = [t for i, t in enumerate(tasks) if i >= 10 or i not in priority_indices]
            return prioritized + remaining
            
        except Exception as e:
            print(f"AI prioritization error: {e}")
            # Fallback to default prioritization
            return sorted(tasks, key=lambda x: (
                -x.get('priority', 3),
                -x.get('impact', 5),
                x.get('due_date', datetime.max)
            ))

    def generate_recommendations(self, tasks):
            """Generate AI recommendations from task data"""
            logger.info(f"AI Helper called with {len(tasks) if tasks else 0} tasks")

            if not tasks:
                logger.info("No tasks provided, returning default recommendations")
                return self._get_default_recommendations()

            # Check if OpenAI API key is configured
            api_key = current_app.config.get('OPENAI_API_KEY')
            logger.info(f"OpenAI API key configured: {'YES' if api_key else 'NO'}")

            if not api_key:
                logger.warning("OpenAI API key not found in config. Using default recommendations.")
                return self._get_default_recommendations()

            try:
                openai.api_key = api_key

                # Prepare task summary
                task_summary = "\n".join([
                    f"- {t.title} (Priority: {t.priority}, Status: {t.status}, Due: {t.due_date.strftime('%Y-%m-%d') if t.due_date else 'N/A'})"
                    for t in tasks[:8]  # Limit to 8 tasks to avoid token limits
                ])

                prompt = f"""Based on these tasks, provide productivity recommendations in JSON format:
    {task_summary}

    Return JSON with these fields:
    - focus_areas: list of 2-3 area recommendations
    - quick_wins: list of 2 achievable quick wins
    - risk_alerts: list of 2 potential risks
    - optimization_tips: list of 2-3 tips to improve efficiency
    - efficiency_score: 0-100 score

    Return ONLY valid JSON, no other text."""

                logger.info("Sending request to OpenAI API...")

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )

                content = response.choices[0].message.content.strip()
                logger.info(f"OpenAI raw response: {content[:200]}...")  # Log first 200 chars

                recommendations = json.loads(content)

                logger.info("Successfully parsed OpenAI response")

                return {
                    'focus_areas': list(recommendations.get('focus_areas', [])),
                    'quick_wins': list(recommendations.get('quick_wins', [])),
                    'risk_alerts': list(recommendations.get('risk_alerts', [])),
                    'optimization_tips': list(recommendations.get('optimization_tips', [])),
                    'efficiency_score': int(recommendations.get('efficiency_score', 70))
                }

            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error from OpenAI: {e}")
                return self._get_default_recommendations()
            except openai.error.AuthenticationError as e:
                logger.error(f"OpenAI Authentication Error: {e}")
                return self._get_default_recommendations()
            except openai.error.RateLimitError as e:
                logger.error(f"OpenAI Rate Limit Error: {e}")
                return self._get_default_recommendations()
            except openai.error.APIError as e:
                logger.error(f"OpenAI API Error: {e}")
                return self._get_default_recommendations()
            except Exception as e:
                logger.error(f"Unexpected error in AI recommendations: {e}")
                return self._get_default_recommendations()
    
    def _get_default_recommendations(self):
        """Return default recommendations when AI is unavailable"""
        return {
            'focus_areas': ['High priority tasks', 'Overdue items'],
            'quick_wins': ['Complete in-progress tasks first'],
            'risk_alerts': ['Check for dependencies'],
            'optimization_tips': ['Schedule focused time blocks', 'Break large tasks into subtasks'],
            'efficiency_score': 60
        }