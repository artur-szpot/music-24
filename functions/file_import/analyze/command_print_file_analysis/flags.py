from enum import Enum


class PrintFileAnalysisFlags(Enum):
    ShowOnlyIfError = 0
    ShowOnlyIfWarning = 1
    OverwriteCache = 2


print_file_analysis_flags = {
    PrintFileAnalysisFlags.ShowOnlyIfError: ["e", "errors"],
    PrintFileAnalysisFlags.ShowOnlyIfWarning: ["w", "warnings"],
    PrintFileAnalysisFlags.OverwriteCache: ["o", "overwrite"],
}
