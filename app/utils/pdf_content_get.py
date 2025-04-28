import asyncio
from langchain_community.document_loaders import PyPDFLoader
from typing import List, Dict, Any, Tuple

async def load_pdf_pages(start_page: int = 1, end_page: int = 1, file_path: str = "app/algorithms/audit_reference/GB2760-2024.pdf") -> List[Dict[str, Any]]:
    """
    加载PDF文件指定页码范围的内容并返回
    
    Args:
        start_page: 起始页码 (从1开始)
        end_page: 结束页码 (如果为None则加载到最后一页)
    
    Returns:
        包含每页内容和元数据的字典列表
    """
    loader = PyPDFLoader(file_path)
    
    pages = []
    page_idx = 0
    
    async for page in loader.alazy_load():
        page_idx += 1
        if (start_page <= page_idx) and (end_page is None or page_idx <= end_page):
            pages.append({
                "page_number": page_idx,
                "content": page.page_content,
                "metadata": page.metadata
            })
    
    return pages

async def load_pdf_content_as_string(start_page: int = 1, end_page: int = 1, file_path: str = "app/algorithms/audit_reference/GB2760-2024.pdf", separator: str = "\n\n") -> str:
    """
    加载PDF文件指定页码范围的内容并返回为单个字符串
    
    Args:
        start_page: 起始页码 (从1开始)
        end_page: 结束页码 (如果为None则加载到最后一页)
        separator: 页面之间的分隔符
    
    Returns:
        包含所有页面内容的单个字符串
    """
    pages = await load_pdf_pages(start_page, end_page, file_path)
    if not pages:
        return ""
    
    # 将所有页面内容组合成一个字符串
    combined_content = separator.join([page["content"] for page in pages])
    return combined_content


if __name__ == "__main__":
    content_string =  asyncio.run(load_pdf_content_as_string(1, 10, "app/algorithms/audit_reference/添加剂索引表.pdf"))  # 运行异步函数
    print(content_string)