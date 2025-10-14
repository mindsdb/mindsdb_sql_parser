from .agents import CreateAgent, DropAgent, UpdateAgent
from .alter_database import AlterDatabase
from .create_view import CreateView
from .alter_view import AlterView
from .create_database import CreateDatabase
from .create_predictor import CreatePredictor, CreateAnomalyDetectionModel
from .drop_predictor import DropPredictor
from .retrain_predictor import RetrainPredictor
from .finetune_predictor import FinetunePredictor
from .drop_datasource import DropDatasource
from .drop_dataset import DropDataset
from .evaluate import Evaluate
from .latest import Latest
from .create_ml_engine import CreateMLEngine
from .drop_ml_engine import DropMLEngine
from .create_job import CreateJob
from .drop_job import DropJob
from .chatbot import CreateChatBot, UpdateChatBot, DropChatBot
from .trigger import CreateTrigger, DropTrigger
from .knowledge_base import (
    CreateKnowledgeBase, DropKnowledgeBase, CreateKnowledgeBaseIndex, DropKnowledgeBaseIndex, AlterKnowledgeBase,
    EvaluateKnowledgeBase
)

from .skills import CreateSkill, DropSkill, UpdateSkill

# remove it in next release
CreateDatasource = CreateDatabase

