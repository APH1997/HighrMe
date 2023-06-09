import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import ContentCard from "./FeedContentCard"
import "./index.css"
import { getAllPhotosThunk } from "../../store/photos"
import Loader from "../Loader"

function Feed(){
    /*
    Renders a column of content-cards,
    which conditonally render their comments below
    */
    const dispatch = useDispatch()
    const allPhotos = useSelector(state => state.photos.allPhotos)

    useEffect(() => {
        dispatch(getAllPhotosThunk(allPhotos))
    }, [dispatch])

    let sortedPhotos;
    if (!allPhotos){
        return <Loader />
    } else{
        sortedPhotos = Object.values(allPhotos)
        .sort((a,b) =>  new Date(b.created_at) - new Date(a.created_at))
    }

    if (!sortedPhotos) return <Loader />

    return (
            <div className="feed-main-container">

            {sortedPhotos.map(photo => {
                return <ContentCard key={photo.id} photo={photo}/>
            })}
            </div>
    )
}

export default Feed
