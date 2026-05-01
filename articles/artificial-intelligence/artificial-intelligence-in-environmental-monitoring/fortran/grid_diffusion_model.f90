! Artificial Intelligence in Environmental Monitoring
!
! Fortran example:
! Simple grid-based diffusion model for environmental concentration.
!
! Compile:
! gfortran grid_diffusion_model.f90 -o grid_diffusion_model
!
! Run:
! ./grid_diffusion_model

program grid_diffusion_model
  implicit none

  integer, parameter :: nx = 20
  integer, parameter :: ny = 20
  integer, parameter :: nt = 60
  real, parameter :: diffusion = 0.08
  real :: grid(nx, ny)
  real :: next_grid(nx, ny)
  integer :: i, j, t

  grid = 0.0
  grid(nx / 2, ny / 2) = 10.0

  do t = 1, nt
    next_grid = grid

    do i = 2, nx - 1
      do j = 2, ny - 1
        next_grid(i, j) = grid(i, j) + diffusion * ( &
          grid(i + 1, j) + grid(i - 1, j) + &
          grid(i, j + 1) + grid(i, j - 1) - &
          4.0 * grid(i, j))
      end do
    end do

    grid = next_grid
  end do

  print *, "Final center concentration:", grid(nx / 2, ny / 2)
  print *, "Final corner concentration:", grid(2, 2)

end program grid_diffusion_model
