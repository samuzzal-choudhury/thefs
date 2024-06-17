"""API to support storage operations."""

from flask import Blueprint, jsonify, request
from thefs.utils.files import FileUtils
from thefs.utils.log import logger

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

response = {'message': 'success'}
futil = FileUtils()


@api_v1.route('/', methods=['GET'])
def root():
    """Root endpoint which is not available for use."""
    logger.info("Endpoint is unavailable.")
    return jsonify({'error': 'This endpoint is not available'}), 404


@api_v1.route('/liveness', methods=['GET'])
def liveness():
    """Liveness endpoint to check if the system is up."""
    logger.info("The system is available")
    return jsonify({}), 200


@api_v1.route('/readiness', methods=['GET'])
def readiness():
    """Readiness endpoint to check if the system is running."""
    if futil.dir:
        logger.info("Storage directory is available. System is ready to run")
        return jsonify({}), 200
    return jsonify({'error': 'Storage directory is unavailable.'
                             ' Server not ready'}), 500


@api_v1.route('/add', methods=['POST'])
def add_files():
    """Endpoint to add new files to the storage."""
    existing_files = futil.list_files()

    if request.method == 'POST':
        filelist = request.files.getlist('files')
        for file in filelist:
            if file.filename in existing_files:
                return jsonify({'error': f'Received an existing '
                                         f'file {file.filename}'}), 400
            if not futil.store_file(file.filename, file):
                return jsonify({'error': 'Invalid file uploaded.'}), 400
        return jsonify(response), 200

    return jsonify({'error': 'Unsupported method'}), 405


@api_v1.route('/list', methods=['GET'])
def list_files():
    """Endpoint to list all files in the storage."""
    if request.method == 'GET':
        return jsonify(futil.list_files()), 200
    return jsonify({'error': 'Unsupported method'}), 405


@api_v1.route('/update', methods=['PUT'])
def update_file():
    """Endpoint to update a file to the storage."""
    if request.method == 'PUT':
        filelist = request.files.getlist('files')
        print(filelist)
        for file in filelist:
            if not futil.store_file(file.filename, file):
                return jsonify({'error': 'Invalid file uploaded.'}), 400
        return jsonify(response), 200

    return jsonify({'error': 'Unsupported method'}), 405


@api_v1.route('/remove', methods=['DELETE'])
def remove_file():
    """Endpoint to remove a file to the storage."""
    if request.method == 'DELETE':
        fname = request.form.get('filename')
        if fname:
            if not futil.remove_file(fname):
                return jsonify({'error': 'File deletion unsuccessful. '
                                         'Invalid parameter.'}), 400
            else:
                return jsonify({'status': f'successfully '
                                          f'deleted {fname}'}), 200
        else:
            return jsonify({'error': 'Invalid file parameter'}), 400
    return jsonify({'error': 'Unsupported method'}), 405


@api_v1.route('/word-count', methods=['GET'])
def count_total_words():
    """Endpoint to get the word count of all the files in the storage."""
    if request.method == 'GET':
        return jsonify(futil.count_total_words()), 200
    return jsonify({'error': 'Unsupported method'}), 405


@api_v1.route('/freq-words', methods=['GET'])
def get_freq_words():
    """Endpoint to get the list of first n frequent words available."""
    if request.method == 'GET':
        limit, order = request.args.get('limit'), request.args.get('order')
        words = futil.generate_words_frequency(limit, order)
        if len(words) > 0:
            return jsonify(words), 200
        else:
            return jsonify({'error': 'Unsupported arguments received'}), 400
    return jsonify({'error': 'Unsupported method'}), 405
