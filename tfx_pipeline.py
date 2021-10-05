from tfx import v1 as tfx
import os

PIPELINE_NAME = "connect4-trainer"

# Output directory to store artifacts generated from the pipeline.
PIPELINE_ROOT = os.path.join('pipelines', PIPELINE_NAME)
# Path to a SQLite DB file to use as an MLMD storage.
METADATA_PATH = os.path.join('metadata', PIPELINE_NAME, 'metadata.db')
# Output directory where created models from the pipeline will be exported.
SERVING_MODEL_DIR = os.path.join('serving_model', PIPELINE_NAME)

_data_filepath = 'results/all_results.csv'


def _create_pipeline(pipeline_name: str, pipeline_root: str, data_root: str,
                     serving_model_dir: str,
                     metadata_path: str) -> tfx.dsl.Pipeline:

  example_gen = tfx.components.CsvExampleGen(input_base=_data_filepath)

  trainer = tfx.components.Trainer(
      module_file='Trainer.py',
      examples=example_gen.outputs['examples'],
      train_args=tfx.proto.TrainArgs(num_steps=100),
      eval_args=tfx.proto.EvalArgs(num_steps=5))



  components = [
    trainer

  ]

  return tfx.dsl.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(metadata_path),
      components=components)



tfx.orchestration.LocalDagRunner().run(
  _create_pipeline(
      pipeline_name=PIPELINE_NAME,
      pipeline_root=PIPELINE_ROOT,
      data_root='s',
      serving_model_dir=SERVING_MODEL_DIR,
      metadata_path=METADATA_PATH))
