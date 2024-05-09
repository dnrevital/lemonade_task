# Lemonade Home Assignment 

## Thought Process
Finding the bottleneck of this solution regarding:
- Complexity 
- Speed
- Memory
- Development of additional requirement which may arrise in the product's lifetime.
  
Found a need to improve:
- Semantic Search
- Decision Algorithm (given top-n, decide which is the right answer)

I analyzed that using a Semantic Database for the semantic search works better for this product, for the following reasons:

- Efficiency:

Faster Search: A Vector DB is optimized for efficient nearest neighbor search in high-dimensional vector spaces. It utilizes techniques like locality-sensitive hashing (LSH) to perform faster approximate nearest neighbor searches compared to a brute-force KNN search, especially when dealing with large datasets of embeddings.
   
- Scalability:

Handling Large Datasets: 
		
A Vector DB can efficiently handle large collections of vector embeddings, making it suitable for scenarios where you have a vast number of macros to search through. As the macro collection grows, a Vector DB maintains its search speed advantage.

- Memory Management:

Reduced Memory Consumption: A Vector DB can be more memory-efficient than a naive KNN implementation, particularly when dealing with high-dimensional vectors. It utilizes techniques like indexing and compression to store and access embeddings efficiently.
			
- Integration:

A Vector DB readily integrates with vector database solutions, allowing to store and manage the macro embeddings alongside additional metadata if needed. This facilitates a more structured and scalable approach to semantic search.	

## Improvements for Described Solution

1. Use a Vector DB rather than KNN for the semantic search (advantages are explained above).
2. Consider the user's metadata for matching the question to a macro. We can add semantic embeddings of texts we have from this user (previous questions, descirption), as well as a vector representation of non-semantic features known from the metadata.
3. Index in the Senatic DB the annotated examples (1M+ as described), and use them to enhance the accuracy of the matching macros. 

## My Solution

As guided, I mocked most parts pf the solution, to fit it with the scope of this submission. I'll explain below, for each of the solution's components:
- What I'd develop for a real product
- What I developed for this submission

### Service / Endpoint
- Real Product. A web client should be developed with most SOTA front-end tools and graphics.

- Submission. I used python Flask, as I don't have much experience with TypeScript. I understand this is fine in the case. I further assume that the focus of this exercise is about the semantic search and the matching capability, and less about how this part is omplemented. 

### Macro Preprocessing

For both real product and this submission, there needs to be a good representation, by semantic embeddings, of the macro. We want to uitlize all available texts of the macro.

Both real-product and submission need to preprocess the texts.

In a real product:
- Generate an embedding vector based on concatenation of the macro's texts, such as description, name, intent and the like. Index it in the Vector DB, with the macro no. as a document. 
- Generate embeddings of each of the 1M+ available annotated examples, and index each of them with the macro no. as a document.

In the submission:
- I generated an embedding based on the macro's texts and indexed it in the Vector DB, with the macro no. as the indexed document. 

### Embedding Generation

For both real product and this submission, we need the embeddings to represent a whole sentence or paragraph, rather than single words. This allows for a best matching of the question and customer details to the macro's texts.

- Real Product. 
A real product would allow me to use a large model for embeddings generation. I'd either use an LLM API (like OpenAI API) to retrieve the sentence embedding, or use a sufficiently large and good-performing model (e.g. Gemma 2B/7B) deployed in the cloud (packaged as Docker, deployed as serverless ["Lambda Function"]).

- Submission.
I am using sentence-t5-base from HuggingFace's sentence-transformers library, which seems to provide a pretty good macro fitting in this scope. 

### Semantic Search

As explained in the Thought Process paragraph, I rather using a Semantic DB rather than KNN. 

- Real Product.
I'd use an advanced online/cloud solution such as Pinecone, which is suitable for a large scale, and supports dense and sparse vectors, so I can leverage the usage of embeddings to many types of data. 

- Submission.
I am using Faiss CPU version, which is a free, library version (no need overload the code with secret-key management, web API's etc.), very suitable for small-scale exercise environments like this one. Yet it makes a pretty good job for this scale. 

### Question Preprocessing

- Real Product.
Use the embedding egenration model to generate a semantic embedding of the question's text. Use custom functions to translate as many as can customer-data fields into embeddings (not necessarily semantic embeddings). 

- Submission.
Generating the semantic embedding of the question's text using the sentence-t5-based model. 

### Postprocessing

- Real Product.
The semantic search considers all indexed macro texts and examples. Receive the top-n matching indices from the Semantic DB. narrow down the results by voting (majority wins), or by further focused search in the Vector DB, considering all relevant dense and sparse vectors. 

The client side fills-in the placeholders of the macro's Content field with the relevant customer-data, and prints the formatted answer. 

- Submission.
Take the single best-fitting vector, return the indexed document's (macro no.) macro ID. the client-side prints the result as is.

### Assumptions

- The macros' contents are already tested and verified by the domain professionals, including their metadata, content, intent and input examples.
- For the submission - the client-side enters legal texts as relevant. Correctness and basic errors aren't verified. 

### Running the Submission


- Installation of Required Libraries
```
pip install -r requirements.txt
```

- Running the Server Side
``` 
python -m chat_service
```

- Running the Client Side
```
python -m chat_client
```

### Metrics

To check for the quality of the results, the main measure should be accuracy, measured as:

(queries where the resulting macro fits the ground-truth macro) / (all queries with a ground-truth)

Other measures that can be taken are more sophisticated text-matching measures, used in the GenAI domain, e.g. BLEU, measured by comparing the returned macro text to the ground-truth text. 

In these cases, even if we haven't returned the correct macro number, by the text of the returned macro is similar to the text of the fitting macro, the score will be relatively high. 

### Examples from Running this Submission

Enter your question: Why aren't pet policies are available at Florida?
Enter your active policies (e.g., Car, Other): pet
Enter your timezone (e.g., America/LA): America
Selected Answer (Macro): macro_001_pet_update_address_uncovered_state

Enter your question: Can I update my address?
Enter your active policies (e.g., Car, Other): pet
Enter your timezone (e.g., America/LA): America
Selected Answer (Macro): macro_002_pet_update_address_same_premium

Enter your question: Why can't you insure me?
Enter your active policies (e.g., Car, Other): Car
Enter your timezone (e.g., America/LA): PST
Selected Answer (Macro): macro_003_dunning_setup_new
