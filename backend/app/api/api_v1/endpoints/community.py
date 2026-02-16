from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.community import CommunityPost, CommunityComment

router = APIRouter()


@router.get("/posts")
async def get_community_posts(
    limit: int = 20,
    offset: int = 0,
    post_type: Optional[str] = None,
    crop_category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get community posts
    """
    try:
        query = db.query(CommunityPost).filter(CommunityPost.is_approved == True)
        
        if post_type:
            query = query.filter(CommunityPost.post_type == post_type)
        
        if crop_category:
            query = query.filter(CommunityPost.crop_category == crop_category)
        
        posts = query.order_by(CommunityPost.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "post_type": post.post_type,
                    "crop_category": post.crop_category,
                    "topic_tags": post.topic_tags,
                    "likes_count": post.likes_count,
                    "comments_count": post.comments_count,
                    "views_count": post.views_count,
                    "is_featured": post.is_featured,
                    "is_pinned": post.is_pinned,
                    "language": post.language,
                    "created_at": post.created_at,
                    "user": {
                        "id": post.user.id,
                        "name": post.user.name,
                        "district": post.user.district,
                        "state": post.user.state
                    }
                }
                for post in posts
            ],
            "total": len(posts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching community posts: {str(e)}")


@router.post("/posts")
async def create_community_post(
    title: str,
    content: str,
    post_type: str,
    crop_category: Optional[str] = None,
    topic_tags: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new community post
    """
    try:
        post = CommunityPost(
            user_id=current_user.id,
            title=title,
            content=content,
            post_type=post_type,
            crop_category=crop_category,
            topic_tags=topic_tags,
            language=current_user.preferred_language
        )
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        return {
            "message": "Post created successfully",
            "post_id": post.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")


@router.get("/posts/{post_id}")
async def get_community_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific community post with comments
    """
    try:
        post = db.query(CommunityPost).filter(
            CommunityPost.id == post_id,
            CommunityPost.is_approved == True
        ).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Increment view count
        post.views_count += 1
        db.commit()
        
        # Get comments
        comments = db.query(CommunityComment).filter(
            CommunityComment.post_id == post_id,
            CommunityComment.is_approved == True
        ).order_by(CommunityComment.created_at.asc()).all()
        
        return {
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "post_type": post.post_type,
                "crop_category": post.crop_category,
                "topic_tags": post.topic_tags,
                "likes_count": post.likes_count,
                "comments_count": post.comments_count,
                "views_count": post.views_count,
                "is_featured": post.is_featured,
                "is_pinned": post.is_pinned,
                "language": post.language,
                "created_at": post.created_at,
                "user": {
                    "id": post.user.id,
                    "name": post.user.name,
                    "district": post.user.district,
                    "state": post.user.state
                }
            },
            "comments": [
                {
                    "id": comment.id,
                    "content": comment.content,
                    "likes_count": comment.likes_count,
                    "language": comment.language,
                    "created_at": comment.created_at,
                    "user": {
                        "id": comment.user.id,
                        "name": comment.user.name,
                        "district": comment.user.district,
                        "state": comment.user.state
                    }
                }
                for comment in comments
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching post: {str(e)}")


@router.post("/posts/{post_id}/like")
async def like_community_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Like a community post
    """
    try:
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        post.likes_count += 1
        db.commit()
        
        return {"message": "Post liked successfully", "likes_count": post.likes_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error liking post: {str(e)}")


@router.post("/posts/{post_id}/comments")
async def comment_on_post(
    post_id: int,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a comment to a community post
    """
    try:
        # Check if post exists
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        comment = CommunityComment(
            post_id=post_id,
            user_id=current_user.id,
            content=content,
            language=current_user.preferred_language
        )
        
        db.add(comment)
        
        # Increment comment count
        post.comments_count += 1
        db.commit()
        
        return {
            "message": "Comment added successfully",
            "comment_id": comment.id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding comment: {str(e)}")


@router.get("/trending")
async def get_trending_posts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get trending community posts
    """
    try:
        posts = db.query(CommunityPost).filter(
            CommunityPost.is_approved == True
        ).order_by(
            CommunityPost.likes_count.desc(),
            CommunityPost.comments_count.desc(),
            CommunityPost.views_count.desc()
        ).limit(limit).all()
        
        return {
            "trending_posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content[:200] + "..." if len(post.content) > 200 else post.content,
                    "post_type": post.post_type,
                    "crop_category": post.crop_category,
                    "likes_count": post.likes_count,
                    "comments_count": post.comments_count,
                    "views_count": post.views_count,
                    "created_at": post.created_at,
                    "user": {
                        "id": post.user.id,
                        "name": post.user.name,
                        "district": post.user.district,
                        "state": post.user.state
                    }
                }
                for post in posts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending posts: {str(e)}")
