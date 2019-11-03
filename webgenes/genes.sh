#!/usr/bin/bash

function genes() {
  stty -echo

  echo -e '\033[1m\033[33mStart WebGenes\033[0m'

  echo 'Initial checks in progress...'
  echo -e '   0%  ~~~~~~~~~~~~~~~~~~~~'

  command python3 -V > /dev/null 2>&1

  if [[ $? -eq 127 ]]; then
    echo -e '\033[A\033[AInitial checks failed.\033[K\n  0%  \033[1m\033[31m-------\033[0m~~~~~~~~~~~~~'
    echo 'Python3 not installed. Aborting.'
    read -t 1 -n 10000 discard
    stty echo
    return 200
  fi

  echo -e '\033[A  33%  \033[1m\033[32m+++++++\033[0m~~~~~~~~~~~~~'

  if [[ $WEBGENES_PATH == '' ]]; then
    echo -e '\033[A\033[AInitial checks failed.\033[K\n  33%  \033[1m\033[32m+++++++\033[31m------\033[0m~~~~~~~'
    echo '$WEBGENES_PATH is not set. Aborting.'
    read -t 1 -n 10000 discard
    stty echo
    return 201
  fi

  if [[ ! -d $WEBGENES_PATH ]]; then
    echo -e '\033[A\033[AInitial checks failed.\033[K\n  33%  \033[1m\033[32m+++++++\033[31m------\033[0m~~~~~~~'
    echo '$WEBGENES_PATH does not contain a valid path'
    read -t 1 -n 10000 discard
    stty echo
    return 202
  fi

  if [[ $WEBGENES_PATH != *'/' ]]; then
    export WEBGENES_PATH=${WEBGENES_PATH}/
  fi

  echo -e '\033[A  67%  \033[1m\033[32m+++++++++++++\033[0m~~~~~~~'

  if [[ $WEBGENES_PATH != '/'* ]]; then
    export WEBGENES_PATH=${PWD}/${WEBGENES_PATH}
  fi

  echo -e '\033[A\033[AInitial checks completed.\033[K\n 100%  \033[1m\033[32m++++++++++++++++++++\033[0m'

  python3 ${WEBGENES_PATH}genes.py $@

  exit_code=$?

  read -t 1 -n 10000 discard
  stty echo

  return $exit_code
}
