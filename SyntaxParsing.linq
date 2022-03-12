<Query Kind="Program" />

private string[] corruptedLines = new[] {
	"{([(<{}[<>[]}>{[]{[(<()>",
	"[[<[([]))<([[{}[[()]]]",
	"[{[{({}]{}}([{[{{{}}([]",
	"[<(<(<(<{}))><([]([]()",
	"<{([([[(<>()){}]>(<<{{"
};

private string[] allLines = new[] {
		"[({(<(())[]>[[{[]{<()<>>",
		"[(()[<>])]({[<{<<[]>>(",
		"{([(<{}[<>[]}>{[]{[(<()>",
		"(((({<>}<{<{<>}{[]{[]{}",
		"[[<[([]))<([[{}[[()]]]",
		"[{[{({}]{}}([{[{{{}}([]",
		"{<[[]]>}<{[{[{[]{()[[[]",
		"[<(<(<(<{}))><([]([]()",
		"<{([([[(<>()){}]>(<<{{",
		"<{([{{}}[<[[[<>{}]]]>[]]",
		"([{<({<[{<([])>}]>})>}])" // Added a valid line just to make sure that this works - will be covered in Unit Tests in the full solution
};

void Main()
{
	foreach (var line in allLines)
	{
		ProcessLine(line);
	}
}

public ProcessLineResult ProcessLine(string line)
{
	Chunk? currentChunk = null;

	// Although at this point we don't know how many Chunks we will find, it cannot be more than the characters in the line
	var parsedChunks = new List<Chunk>(line.Length);

	for (var lineIndex = 0; lineIndex < line.Length; lineIndex++)
	{
		switch (line[lineIndex])
		{
			case '<':
			case '{':
			case '(':
			case '[':
				if (currentChunk is null)
				{
					currentChunk = new Chunk(line[lineIndex], lineIndex);

					parsedChunks.Add(currentChunk);

					continue;
				}

				var childChunk = new Chunk(line[lineIndex], lineIndex, currentChunk);

				parsedChunks.Add(childChunk);

				currentChunk = childChunk;

				continue;

			case '>':
			case '}':
			case ')':
			case ']':

				if (currentChunk is not null && currentChunk.TryEndChunk(line[lineIndex], lineIndex))
				{
					currentChunk = currentChunk.Parent;

					continue;
				}

				Console.WriteLine($"Unexpected character at index {lineIndex} in line {line}");

				return ProcessLineResult.CorruptedResult(lineIndex);
		}

		break;
	}

	// If we get to this point then we haven't found any rogue end tags, do we have any unclosed chunks

	var firstUnclosedChunk = parsedChunks.FirstOrDefault(c => c.EndIndex is null);

	if (firstUnclosedChunk is null)
	{
		Console.WriteLine($"Successful line {line}");

		return ProcessLineResult.SuccessResult(); // If we reach here then all pairs were successfully matched
	}

	Console.WriteLine($"Unclosed chunk at starting index {firstUnclosedChunk.StartIndex} in line {line}");

	return ProcessLineResult.IncompleteResult(firstUnclosedChunk.StartIndex);
}

public enum LineStatus
{
	ParsedSuccessfully = 1,
	Corrupted = 2,
	Incomplete = 3
}

public class ProcessLineResult
{
	private ProcessLineResult(LineStatus lineStatus, int? failureIndex = null)
	{
		LineStatus = lineStatus;
		FailureIndex = failureIndex;
	}

	public LineStatus LineStatus { get; }

	public int? FailureIndex { get; }

	public static ProcessLineResult SuccessResult()
	{
		return new ProcessLineResult(LineStatus.ParsedSuccessfully);
	}

	public static ProcessLineResult CorruptedResult(int failureIndex)
	{
		return new ProcessLineResult(LineStatus.Corrupted, failureIndex);
	}

	public static ProcessLineResult IncompleteResult(int failureIndex)
	{
		return new ProcessLineResult(LineStatus.Incomplete, failureIndex);
	}
}

public class Chunk
{
	public Chunk(char startCharacter, int startIndex)
	{
		StartCharacter = startCharacter;
		StartIndex = startIndex;
	}

	public Chunk(char startCharacter, int startIndex, Chunk parent) : this(startCharacter, startIndex)
	{
		Parent = parent;
	}

	public char StartCharacter { get; }

	public int StartIndex { get; }

	public char? EndCharacter { get; private set; }

	public int? EndIndex { get; private set; }

	public Chunk? Parent { get; }

	public bool TryEndChunk(char endCharacter, int endIndex)
	{
		switch (endCharacter)
		{
			case '>' when StartCharacter == '<':
			case '}' when StartCharacter == '{':
			case ')' when StartCharacter == '(':
			case ']' when StartCharacter == '[':
				EndCharacter = endCharacter;

				EndIndex = endIndex;

				return true;
			default:
				return false;
		}
	}
}