# RAG Strategy Pattern

## 使用例

```python
# ユースケース層での使用
class ExecuteRAGUseCase:
    def __init__(self, rag_strategy: RAGStrategy):
        self.rag_strategy = rag_strategy
    
    async def execute(self, query_text: str) -> QueryResult:
        query = Query(text=query_text)
        return await self.rag_strategy.execute(query)
```

```python
# インフラストラクチャ層での実装例
class SimpleRAGStrategy(RAGStrategy):
    def __init__(self, 
                 document_repository: DocumentRepository,
                 openai_client: AzureOpenAIClient):
        super().__init__(document_repository)
        self.openai_client = openai_client
    
    async def execute(self, query: Query) -> QueryResult:
        # 1. クエリのエンベディング生成
        query.embedding = await self._generate_embedding(query.text)
        
        # 2. 類似ドキュメント検索
        documents = await self.document_repository.search(
            query_embedding=query.embedding,
            top_k=query.top_k,
            filters=query.filters
        )
        
        # 3. コンテキストから回答生成
        answer = await self._generate_answer(query.text, documents)
        
        # 4. 結果を構築
        return QueryResult(
            query=query,
            documents=[doc.to_dict() for doc in documents],
            answer=answer,
            sources=[doc.source for doc in documents if doc.source]
        )
    
    async def _generate_embedding(self, text: str) -> list[float]:
        # Azure OpenAI エンベディング実装
        pass
    
    async def _generate_answer(self, query: str, documents: list[Document]) -> str:
        # Azure OpenAI LLM実装
        pass
```

## 利点

1. **シンプルなインターフェース**: 1つのメソッドでRAG全体を実行
2. **実装の柔軟性**: 各戦略が内部でどのようにRAGを実現するかは自由
3. **テストの容易さ**: モックしやすいシンプルなインターフェース
4. **拡張性**: 新しいRAG手法（GraphRAG、HybridRAGなど）を簡単に追加可能