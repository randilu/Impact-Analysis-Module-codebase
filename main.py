from src.data.trend_data import fetch_trend_data_with_date
from src.features.handle_dup_kw import event_vector_dup_kw

# print(fetch_trend_data_with_date.py)
# event_vector_dup_kw.py


# def main():
#     try:
#     from src.data.trend_data import fetch_trend_data_with_date
#
#     from src.features.handle_dup_kw import event_vector_dup_kw
#
#     system_major = sys.version_info.major
#     if REQUIRED_PYTHON == "python":
#         required_major = 2
#     elif REQUIRED_PYTHON == "python3":
#         required_major = 3
#     else:
#         raise ValueError("Unrecognized python interpreter: {}".format(
#             REQUIRED_PYTHON))
#
#     if system_major != required_major:
#         raise TypeError(
#             "This project requires Python {}. Found: Python {}".format(
#                 required_major, sys.version))
#     else:
#         print(">>> Development environment passes all tests!")
#
#
# if __name__ == '__main__':
#     main()
