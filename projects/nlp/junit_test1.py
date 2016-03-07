#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

helpStr = """
  Simple script to run unit test 1:

  The dataset is categories defined by base sentences (each with ten words).
  For each base sentence there are five new sentences each, with an additional
  word substitution that does not change the meaning of the sentence. For the
  test we use each of the sentences as a search term. A perfect result ranks the
  four similar sentences closest to the search.
"""

import argparse

from htmresearch.support.junit_testing import (
  printRankResults, setupExperiment, testModel)



def runExperiment(args):
  """ Build a model and test it."""
  model, dataSet = setupExperiment(args)

  ranks = testModel(model,
                    dataSet,
                    categorySize=6,
                    verbosity=args.verbosity)
  printRankResults("JUnit1", ranks)

  return model



if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=helpStr
  )

  parser.add_argument("-c", "--networkConfigPath",
                      default="data/network_configs/sensor_knn.json",
                      help="Path to JSON specifying the network params.",
                      type=str)
  parser.add_argument("-m", "--modelName",
                      default="htm",
                      type=str,
                      help="Name of model class. Options: [keywords,htm]")
  parser.add_argument("--modelDir",
                      default="MODELNAME.checkpoint",
                      help="Model will be saved in this directory.")
  parser.add_argument("--retina",
                      default="en_associative_64_univ",
                      type=str,
                      help="Name of Cortical.io retina.")
  parser.add_argument("--apiKey",
                      default=None,
                      type=str,
                      help="Key for Cortical.io API. If not specified will "
                      "use the environment variable CORTICAL_API_KEY.")
  parser.add_argument("-v", "--verbosity",
                      default=1,
                      type=int,
                      help="verbosity 0 will print out experiment steps, "
                           "verbosity 1 will include results, and verbosity > "
                           "1 will print out preprocessed tokens and kNN "
                           "inference metrics.")
  args = parser.parse_args()

  # By default set checkpoint directory name based on model name
  if args.modelDir == "MODELNAME.checkpoint":
    args.modelDir = args.modelName + ".checkpoint"

  # Default dataset for this unit test
  args.dataPath = "data/junit/unit_test_1.csv"

  model = runExperiment(args)