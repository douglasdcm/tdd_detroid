NUI=$1
SNUI=$2
python cli.py list-db
CMD="python cli.py student"
${CMD} --help
${CMD} add-info --help
${CMD} add-info --nui ${NUI} --name "ANY" --age "42"
${CMD} subscribe --nui ${NUI} --snui ${SNUI}
${CMD} list-info --nui ${NUI}
echo ""
${CMD} list-subjects --nui ${NUI}

