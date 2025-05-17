def generate_mock_fastq(prefix,read_count=1000000, read_len=150):
    def make_seq(base1, base2):
        return (base1 + base2) * (read_len // 2)

    with open(f"{prefix}_R1.fastq", "w") as r1, open(f"{prefix}_R2.fastq", "w") as r2:
        for i in range(1, read_count + 1):
            read_id = f"{prefix}_read{i:04d}"
            seq1 = make_seq("A", "C")[:read_len]
            seq2 = make_seq("T", "G")[:read_len]
            qual = "F" * read_len

            r1.write(f"@{read_id}/1\n{seq1}\n+\n{qual}\n")
            r2.write(f"@{read_id}/2\n{seq2}\n+\n{qual}\n")

mock_samples = ["mockA", "mockB"]

for mock in mock_samples:


    generate_mock_fastq(mock,
                        read_count = 1000000,
                        read_len=150)