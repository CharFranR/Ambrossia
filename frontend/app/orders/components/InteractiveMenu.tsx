'use client'

import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardDescription, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { PlusCircle } from 'lucide-react'
import Image from 'next/image'

type MenuItem = {
  id: number
  name: string
  description: string
  image: string
  price: number
}

const menuItems: MenuItem[] = [
  {
    id: 1,
    name: 'Garfield Lasagna',
    description: 'Classic lasagna with tomato, mozzarella & basil.',
    image: '/Lasagna.jpg',
    price: 8.5,
  },
  {
    id: 2,
    name: 'Papyrus Spaguetti',
    description: 'Spaguetti with pancetta & parmesan cheese.',
    image: '/Spaguetti.jpg',
    price: 10.0,
  },
  {
    id: 3,
    name: 'Slurp',
    description: 'The clasic and favorite slurp flavor for all the family.',
    image: '/Slurp.jpg',
    price: 6.5,
  },
  {
    id: 4,
    name: 'Roast Basilisk',
    description: 'A well cooked basilisk with a side of garlic and herbs.',
    image: '/Roast_Basilisk.png',
    price: 8.5,
  },
  {
    id: 5,
    name: 'Max Energy Drink!',
    description: 'Perfect drink for speedtesters who wants to die by a heart attack.',
    image: '/max_energy_drink.jpg',
    price: 6.5,
  },
  {
    id: 6,
    name: 'Blood Bag',
    description: 'Preferred by the chef and the most popular on demand!.',
    image: '/power_special.jpg',
    price: 6.5,
  },
]

export default function InteractiveMenu() {
  const handleAdd = (item: MenuItem) => {
    console.log('Added:', item)
  }

  return (
    <div className="p-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {menuItems.map((item) => (
        <motion.div
          key={item.id}
          whileHover={{ scale: 1.03 }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: item.id * 0.1, duration: 0.4 }}
        >
          <Card className="overflow-hidden rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 bg-black">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">{item.name}</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </CardHeader>
            <CardContent className="p-0 relative">
              <Image
                src={item.image}
                alt={item.name}
                className="aspect-video object-cover w-full h-56 rounded-b-2xl"
                width={500}
                height={500}
              />
              <div className="absolute bottom-3 right-3">
                <Button
                  variant="default"
                  size="sm"
                  className="flex items-center gap-1 bg-white-600 hover:bg-white-700"
                  onClick={() => handleAdd(item)}
                >
                  <PlusCircle className="h-4 w-4" /> Add
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
