def reciprocal_rank_fusion(
    rank_lists,
    k=60,
    top_k=10
):
    chunk_scores = {}

    for rank_list in rank_lists:

        for index, chunk in enumerate(rank_list):

            contribution = 1 / (k + index + 1)

            chunk_id = chunk["id"]

            chunk_scores[chunk_id] = (
                chunk_scores.get(chunk_id, 0)
                + contribution
            )

    top_results = [
        {
            "id": chunk_id,
            "score": score
        }
        for chunk_id, score in chunk_scores.items()
    ]

    top_results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    top_results = top_results[:top_k]

    for index, result in enumerate(top_results):
        result["rank"] = index + 1

    return top_results