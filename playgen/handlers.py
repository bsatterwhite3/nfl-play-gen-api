import logging
from playgen import filters, playsampler
from playgen.exceptions import InvalidArgumentException, InsufficientDataException

logger = logging.getLogger('app.handlers')


def construct_response(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidArgumentException as e:
            logger.error("Invalid argument provided in request", exc_info=True)
            return "Invalid argument provided in request", 400
        except InsufficientDataException as e:
            logger.error("Request could not be met due to insufficient data", exc_info=True)
            return "Request could not be met due to insufficient data", 404
        except Exception as e:
            logger.error("Encountered error in API", exc_info=True)
            return "Encountered error in API", 500

    return func_wrapper


@construct_response
def get_plays(data, args):
    play_filters = determine_filters_from_query(args)
    with_replacement = args.get('withReplacement', True)
    num_plays = int(args.get('numPlays', 1))

    sampler = playsampler.PlaySampler(data)
    plays = sampler.sample(num_plays, with_replacement=with_replacement, filters=play_filters)
    response = [play.serialize() for play in plays]
    return response, 200


def validate_args(args):
    logger.info(f"ARGS: {args}")
    valid_query_strings = ['numPlays', 'playType', 'withReplacement', 'fieldPosition']
    if any(key not in valid_query_strings for key in args.keys()):
        raise InvalidArgumentException("Invalid query string found in request")
    field_position = args.get('fieldPosition', None)
    if field_position and field_position not in ['behind20', 'between20s', 'redzone', 'goalline']:
        raise InvalidArgumentException(f"Invalid field position : {field_position} found in request")


def determine_filters_from_query(args):
    filter_list = []
    play_type = args.get('playType', None)
    field_position = args.get('fieldPosition', None)

    if play_type:
        filter_list.append(filters.PlayTypeFilter(play_type))

    if field_position:
        filter_list.append(filters.FieldPositionFilter(field_position))
    return filter_list



