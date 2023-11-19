def LIS(arr, order=+1):
    """
    Solving the Longest Increasing Subsequence problem
    set order to -1 for decreasing version
    """
    array = arr[:]
    n = len(array)
    for i in range(n):
        array[i] *= order
    dp = [1 for _ in range(n)]
    par = [-1 for _ in range(n)]
    reverse = [n - 1 - i for i in range(n)]
    for i in reverse:
        for j in [k for k in range(i + 1, n)]:
            if array[i] <= array[j]:
                if dp[i] < dp[j] + 1:
                    dp[i] = dp[j] + 1
                    par[i] = j
    u = -1
    for i in range(n):
        if u == -1 or dp[i] > dp[u]:
            u = i
    seq = []
    uu = u
    while u != -1:
        seq.append(u)
        u = par[u]
    return dp[uu], seq
