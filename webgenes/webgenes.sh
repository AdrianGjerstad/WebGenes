#!/usr/bin/bash

function genes() {
  stty -echo

  echo 'Start WebGenes'

  echo 'Checks in progress...'
  echo -e '  0%  ~~~~~~~~~~~~~~~~~~~~'

  sleep 0.3

  command python3 -V > /dev/null 2>&1

  if [[ $? -eq 127 ]]; then
    echo -e '\033[A\033[AChecks failed.\033[K\n  0%  \033[1m\033[31m----------\033[0m~~~~~~~~~~'
    echo 'Python3 not installed. Aborting.'
    stty echo
    return 200
  fi

  echo -e '\033[A 50%  \033[1m\033[32m++++++++++\033[0m~~~~~~~~~~'

  sleep 0.3

  if [[ $WEBGENES_PATH == '' ]]; then
    echo -e '\033[A\033[AChecks failed.\033[K\n 50%  \033[1m\033[32m++++++++++\033[31m----------\033[0m'
    echo '$WEBGENES_PATH is not set. Aborting.'
    stty echo
    return 201
  fi

  if [[ ! -d $WEBGENES_PATH ]]; then
    echo -e '\033[A\033[AChecks failed.\033[K\n 50%  \033[1m\033[32m++++++++++\033[31m----------\033[0m'
    echo '$WEBGENES_PATH does not contain a valid path'
    stty echo
    return 202
  fi

  if [[ $WEBGENES_PATH != *'/' ]]; then
    export WEBGENES_PATH=${WEBGENES_PATH}/
  fi

  echo -e '\033[A100%  \033[1m\033[32m++++++++++++++++++++\033[0m'

  sleep 0.3

  stty echo
}
