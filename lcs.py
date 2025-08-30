def lcs(S1, S2):
    m = len(S1)
    n = len(S2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    direction = [[""] * (n + 1) for _ in range(m + 1)]  # store arrows

    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S1[i - 1] == S2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                direction[i][j] = "↖"   # diagonal
            elif dp[i - 1][j] >= dp[i][j - 1]:
                dp[i][j] = dp[i - 1][j]
                direction[i][j] = "↑"   # from top
            else:
                dp[i][j] = dp[i][j - 1]
                direction[i][j] = "←"   # from left

    # Backtrack to find LCS string
    i, j = m, n
    lcs_str = []
    while i > 0 and j > 0:
        if direction[i][j] == "↖":
            lcs_str.append(S1[i - 1])
            i -= 1
            j -= 1
        elif direction[i][j] == "↑":
            i -= 1
        else:
            j -= 1
    lcs_str.reverse()

    # Print DP table with arrows
    print("\nDP Table with directions:")
    header = "    " + "   ".join("-" + S2)  # column headers
    print(header)
    for i in range(m + 1):
        row = ["-"] if i == 0 else [S1[i - 1]]
        for j in range(n + 1):
            val = dp[i][j]
            arrow = direction[i][j]
            row.append(f"{val}{arrow}")
        print("   ".join(row))

    return dp[m][n], "".join(lcs_str)


# 🔹 Dynamic input
S1 = input("Enter first string: ")
S2 = input("Enter second string: ")

length, subsequence = lcs(S1, S2)

print("\nLength of LCS:", length)
print("LCS sequence :",subsequence)
