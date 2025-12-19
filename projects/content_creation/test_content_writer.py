import os
from projects.content_creation.agents.content_writer_agent import create_content_writer_agent

def main():
    agent = create_content_writer_agent()
    topic = "Dijital sağlık uygulamalarının hasta bakımına katkıları"
    result = agent.run(topic=topic, content_type="blog_post", word_count=500, tone="professional")
    print(result)
    # Save output
    os.makedirs("outputs", exist_ok=True)
    with open(f"outputs/custom_topic.md", "w", encoding="utf-8") as f:
        f.write(result)
    print("💾 Output saved to outputs/custom_topic.md")

if __name__ == "__main__":
    main()