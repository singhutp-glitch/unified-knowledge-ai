import React from 'react'
import './Citation.css'

const Citation = ({ids,onClick}) => {
  return (
    <button className='citation' onClick={onClick}>
        [{ids.join(', ')}]
    </button>
  )
}

export default Citation