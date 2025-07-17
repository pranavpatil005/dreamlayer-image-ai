from typing import Dict, Any, Optional
from services import (
    generate_hd_image
)

def generate_ad_set(
    api_key: str,
    image: Optional[bytes] = None,
    prompt: Optional[str] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generate a set of product ads based on configuration.
    """
    if not config:
        config = {}
    
    result = {}
    
    if prompt and not image:
        hd_response = generate_hd_image(
            api_key=api_key,
            prompt=prompt,
            num_results=config.get("num_results", 1),
            aspect_ratio=config.get("aspect_ratio", "1:1"),
            sync=config.get("sync", True)
        )
        result["hd_image"] = hd_response
        image = hd_response.get("result_url")
    
    
    return result 