import { useDispatch } from "react-redux"
import { useModal } from "../../context/Modal"
import { useHistory } from "react-router-dom"
import { deleteAlbumThunk } from "../../store/albums"
import { useState } from "react"
import { ThunkHubContext } from "../../context/ThunkHub"
import { useContext } from "react"

function DeleteAlbumModal({album}){
    const {setDestination} = useContext(ThunkHubContext)
    const {closeModal} = useModal()
    const dispatch = useDispatch()
    const history = useHistory()
    const [isDeleting, setIsDeleting] = useState(false)

    async function handleDelete(){
        setIsDeleting(true)
        await dispatch(deleteAlbumThunk(album.id))

        setTimeout(() => setIsDeleting(false), 1500)
        closeModal();

        setDestination(`/users/${album.author.id}`)
        history.push('/thunk/hub')
        
    }
    return (
        <div>
            <h2>Are you sure want to delete this album?</h2>
            <h3>{album.title}: {album.pics.length} photo(s)</h3>
            <p>Photos within this album will NOT be deleted</p>

            <div>
                <button onClick={() => handleDelete()}>
                    {isDeleting ? "Deleting..." : "Delete Album"}
                </button>
                <button onClick={() => closeModal()}>
                    Cancel
                </button>
            </div>
        </div>
    )
}

export default DeleteAlbumModal
