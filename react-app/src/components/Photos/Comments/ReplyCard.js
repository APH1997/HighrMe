import { useState } from "react"
import { NavLink } from "react-router-dom"
import EditComment from "./EditCommentForm"

function ReplyCard({ reply }) {
    const [isEditing, setIsEditing] = useState(false)
    return (
        <div className="comment-card-container reply-container">
            <div className="comment-card-content-container">
                <div>
                    <img id="comment-card-pro-pic" src={reply.author.profile_picture_url}></img>
                </div>
                <div className="comment-card-content">
                    <NavLink to={`/users/${reply.author.id}`}>{reply.author.first_name} {reply.author.last_name}</NavLink>
                    <div className="comment-reply-content-container">
                        {!isEditing && reply.content}
                        {isEditing && <EditComment content={reply} setIsEditing={setIsEditing} reply={true}/>}
                    </div>
                </div>
            </div>
            <div className="comment-reply-author-btns-container">
                <div>
                    <button>
                        <i className="fas fa-edit" onClick={() => setIsEditing(!isEditing)}></i>
                    </button>


                </div>
            </div>
        </div>
    )
}

export default ReplyCard
