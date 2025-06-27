#!/usr/bin/env python3
"""
MCP 连接测试脚本
用于诊断 MCP 服务器连接问题
"""

import asyncio
import json
import sys
from typing import Dict

def test_network_connectivity():
    """测试网络连接"""
    print("=== 测试网络连接 ===")
    try:
        import requests
        url = "https://mcp.api-inference.modelscope.net/d3ee7d0c7acd42/sse"
        response = requests.head(url, timeout=10)
        print(f"✅ 网络连接成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False

def test_mcp_import():
    """测试 MCP 库导入"""
    print("\n=== 测试 MCP 库导入 ===")
    try:
        import mcp
        print("✅ MCP 库导入成功")
        return True
    except ImportError as e:
        print(f"❌ MCP 库导入失败: {e}")
        print("请运行: pip install -U mcp")
        return False

async def test_mcp_connection():
    """测试 MCP 服务器连接"""
    print("\n=== 测试 MCP 服务器连接 ===")
    try:
        from mcp import ClientSession
        from mcp.client.sse import sse_client
        
        url = "https://mcp.api-inference.modelscope.net/d3ee7d0c7acd42/sse"
        headers = {
            "Accept": "text/event-stream",
            "User-Agent": "Qwen-Agent/1.0"
        }
        
        print(f"正在连接到: {url}")
        async with sse_client(url, headers, sse_read_timeout=60) as streams:
            session = ClientSession(*streams)
            async with session:
                await session.initialize()
                print("✅ MCP 服务器连接成功")
                
                # 测试获取工具列表
                try:
                    list_tools = await session.list_tools()
                    print(f"✅ 获取工具列表成功，共 {len(list_tools.tools)} 个工具")
                    for tool in list_tools.tools:
                        print(f"  - {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"⚠️ 获取工具列表失败: {e}")
                
                return True
    except Exception as e:
        print(f"❌ MCP 服务器连接失败: {e}")
        return False

def test_qwen_agent_mcp():
    """测试 Qwen-Agent 的 MCP 集成"""
    print("\n=== 测试 Qwen-Agent MCP 集成 ===")
    try:
        from qwen_agent.tools.mcp_manager import MCPManager
        
        config = {
            "mcpServers": {
                "mcp-yahoo-finance": {
                    "type": "sse",
                    "url": "https://mcp.api-inference.modelscope.net/d3ee7d0c7acd42/sse",
                    "headers": {
                        "Accept": "text/event-stream",
                        "User-Agent": "Qwen-Agent/1.0"
                    },
                    "sse_read_timeout": 60
                }
            }
        }
        
        print("正在初始化 MCP 管理器...")
        manager = MCPManager()
        tools = manager.initConfig(config)
        print(f"✅ MCP 集成成功，获取到 {len(tools)} 个工具")
        
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        return True
    except Exception as e:
        print(f"❌ Qwen-Agent MCP 集成失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🔍 MCP 连接诊断工具")
    print("=" * 50)
    
    # 测试网络连接
    network_ok = test_network_connectivity()
    
    # 测试 MCP 库导入
    mcp_import_ok = test_mcp_import()
    
    if network_ok and mcp_import_ok:
        # 测试 MCP 服务器连接
        mcp_connection_ok = await test_mcp_connection()
        
        if mcp_connection_ok:
            # 测试 Qwen-Agent 集成
            qwen_agent_ok = test_qwen_agent_mcp()
        else:
            qwen_agent_ok = False
    else:
        mcp_connection_ok = False
        qwen_agent_ok = False
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"网络连接: {'✅ 通过' if network_ok else '❌ 失败'}")
    print(f"MCP 库导入: {'✅ 通过' if mcp_import_ok else '❌ 失败'}")
    print(f"MCP 服务器连接: {'✅ 通过' if mcp_connection_ok else '❌ 失败'}")
    print(f"Qwen-Agent 集成: {'✅ 通过' if qwen_agent_ok else '❌ 失败'}")
    
    if all([network_ok, mcp_import_ok, mcp_connection_ok, qwen_agent_ok]):
        print("\n🎉 所有测试通过！MCP 配置正常。")
    else:
        print("\n⚠️ 部分测试失败，请根据上述错误信息进行修复。")
        
        if not network_ok:
            print("\n💡 网络连接问题建议:")
            print("1. 检查网络连接")
            print("2. 检查防火墙设置")
            print("3. 尝试使用代理")
            
        if not mcp_import_ok:
            print("\n💡 MCP 库问题建议:")
            print("1. 运行: pip install -U mcp")
            print("2. 检查 Python 环境")
            
        if not mcp_connection_ok:
            print("\n💡 MCP 服务器连接问题建议:")
            print("1. 检查服务器地址是否正确")
            print("2. 检查是否需要认证")
            print("3. 增加超时时间")
            print("4. 检查服务器状态")

if __name__ == "__main__":
    asyncio.run(main()) 