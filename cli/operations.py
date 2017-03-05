from pydl.models.base.supervised_model import SupervisedModel
from pydl.models.base.unsupervised_model import UnsupervisedModel
from pydl.hyperopt import HyperOptModel, hp_space_from_json, opt_from_config, CVObjectiveFunction
from pydl.datasets.utils import *
from pydl.utils.utilities import load_model, save_json
from pydl.model_selection.metrics import available_metrics
from pydl.model_selection.cv import CV


def fit(config, output):
    """
    """

    print('fit', config)

    m = load_model(config)

    data_set = get_input_data(config)
    x = load_data(data_set, 'train_x')

    if isinstance(m, SupervisedModel):
        y = load_data(data_set, 'train_y')
        m.fit(x_train=x, y_train=y)
    else:
        m.fit(x_train=x)

    # Save model
    m.save_model(output)


def predict(config, output):
    """
    """

    print('predict', config)

    m = load_model(get_model(config))
    assert isinstance(m, SupervisedModel), 'The given model cannot perform predict operation!'

    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')

    preds = m.predict(x)

    # Save predictions as .npy file
    np.save(os.path.join(output, m.name+'_preds.npy'), preds)


def transform(config, output):
    """
    """

    print('transform', config)

    m = load_model(get_model(config))
    assert isinstance(m, UnsupervisedModel), 'The given model cannot perform transform operation!'

    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')

    x_encoded = m.transform(x)

    # Save encoded data in a .npy file
    base_name = os.path.splitext(os.path.basename(data_set['data_x']))[0]
    np.save(os.path.join(output, base_name+'_encoded.npy'), x_encoded)


def reconstruct(config, output):
    """
    """

    print('reconstruct', config)

    m = load_model(get_model(config))
    assert isinstance(m, UnsupervisedModel), 'The given model cannot perform reconstruct operation!'

    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')

    x_rec = m.reconstruct(x)

    # Save reconstructed data in a .npy file
    base_name = os.path.splitext(os.path.basename(data_set['data_x']))[0]
    np.save(os.path.join(output, base_name+'_reconstructed.npy'), x_rec)


def score(config, output):
    """
    """

    print('score', config)

    m = load_model(get_model(config))

    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')

    metrics = config['metrics'] if 'metrics' in config else []

    results = {}
    if isinstance(m, SupervisedModel):
        y = load_data(data_set, 'data_y')

        results[m.get_loss_func()] = m.score(x, y)
        if len(metrics) > 0:
            y_pred = m.predict(x)
            for metric in metrics:
                results[metric] = available_metrics[metric](y, y_pred)

    else:
        results[m.get_loss_func()] = m.score(x)
        if len(metrics) > 0:
            x_rec = m.reconstruct(m.transform(x))
            for metric in metrics:
                results[metric] = available_metrics[metric](x, x_rec)

    # Save results into a JSON file
    save_json(results, os.path.join(output, m.name+'_scores.json'))


def validate(config, output):
    """
    """

    print('validate', config)

    m = load_model(config)

    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')
    y = load_data(data_set, 'data_y')

    # Get validation method
    method, params, metrics = get_cv_config(config)
    cv = CV(method=method, **params)
    results = cv.run(model=m, x=x, y=y, metrics=metrics)

    # Save results into a JSON file
    save_json(results, os.path.join(output, m.name+'_cv.json'))


def optimize(config, output):

    print('optimize', config)

    # Get hp_space
    assert 'hp_space' in config, 'Missing hyperparameters space definition'
    space = hp_space_from_json(config['hp_space'])

    # Get data
    data_set = get_input_data(config)
    x = load_data(data_set, 'data_x')
    y = load_data(data_set, 'data_y') if 'data_y' in data_set else None

    # Get HyperOptModel
    assert 'opt' in config, 'Missing optimizer parameters!'
    opt = get_optimizer(config['opt'])
    obj_fn = get_obj_fn(config['opt'])

    opt_model = HyperOptModel(hp_space=space, fit_fn=obj_fn, opt=opt)
    result = opt_model.fit(x, y, retrain=True)

    print('\n>> Best params =', result['best_model_config'])
    print('\n>> Best fit =', result['opt_result'][1])

    # Save best model
    opt_model.best_model.save_model(output)


#
# UTILS
#
def get_model(config):
    assert 'model' in config, 'Missing model definition!'
    return config['model']


def get_input_data(config):
    assert 'data_set' in config, 'Missing data set path!'
    return config['data_set']


def load_data(data_set, set_name):
    data_path = data_set.get(set_name, None)
    assert data_path is not None and data_path != '', 'Missing %s file!' % set_name
    has_header = data_set.get('has_header', False)
    return load_data_file(data_path, has_header=has_header)


def get_cv_config(config):
    assert 'cv' in config, 'Missing cross-validation configurations!'
    cv_config = config['cv']
    assert 'method' in cv_config, 'Missing cross-validation method!'
    method = cv_config['method']
    params = cv_config['params'] if 'params' in cv_config else {}
    metrics = config['cv']['metrics'] if 'metrics' in config['cv'] else []
    return method, params, metrics


def get_optimizer(config):
    assert 'method' in config, 'Missing optimization method'
    method = config['method']
    params = config['params'] if 'params' in config else {}
    return opt_from_config(method, **params)


def get_obj_fn(config):
    if 'obj_fn' in config:
        obj_fn_config = config['obj_fn']
        cv_method = obj_fn_config['method']
        cv_params = obj_fn_config['params'] if 'params' in obj_fn_config else {}
        return CVObjectiveFunction(cv_method, **cv_params)
    return None
