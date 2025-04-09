import json
import csv
import os


def agg_json(directory, header_list):
    with open(f"{directory}.csv", "w", newline="") as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(header_list)

        # Iterate through each file in the directory
        for file in os.listdir(f"../../raw_data/EMA/response/{directory}"):
            with open(f"../../raw_data/EMA/response/{directory}/{file}") as json_file:
                data = json.load(json_file)
                for row in data:
                    row["user_id"] = file[len(directory) + 1 : -5]
                    values = []
                    for header in header_list:
                        if header in row:
                            values.append(row[header])
                        else:
                            break
                    if len(values) == len(header_list):
                        writer.writerow(values)


if __name__ == "__main__":
    agg_json(
        "Behavior",
        [
            "user_id",
            "anxious",
            "calm",
            "conventional",
            "critical",
            "dependable",
            "disorganized",
            "enthusiastic",
            "experiences",
            "reserved",
            "resp_time",
            "sympathetic",
        ],
    )
    agg_json(
        "Class",
        ["user_id", "course_id", "due", "experience", "hours", "location", "resp_time"],
    )
    agg_json(
        "Mood",
        ["user_id", "happy", "happyornot", "location", "resp_time", "sad", "sadornot"],
    )
    agg_json(
        "Stress",
        ["user_id", "level", "location", "resp_time"],
    )
